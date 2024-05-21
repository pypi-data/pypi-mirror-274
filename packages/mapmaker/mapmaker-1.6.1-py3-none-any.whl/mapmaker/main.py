#!/bin/python
'''The command line interface for mapmaker.'''


import argparse
from collections import namedtuple
import configparser
import io
from pathlib import Path
from pkg_resources import resource_stream
import sys

from . import __author__
from . import __version__
from .geo import distance
from . import icons
from . import parse
from .mapdef import MapParams
from .parse import MapParamsAction
from .parse import FrameAction
from .parse import MarginAction
from .parse import ScaleAction
from .parse import TitleAction, CommentAction
from .service import ServiceRegistry
from .tilemap import MIN_ZOOM, MAX_ZOOM

import appdirs


APP_NAME = 'mapmaker'
APP_DESC = 'Create map images from tile servers.'

Config = namedtuple('Config', ('copyrights'
                               ' cache_limit'
                               ' parallel_downloads'
                               ' icons_base'))


def main():
    '''Parse arguments and run the program.'''
    conf_dir = appdirs.user_config_dir(appname=APP_NAME)
    conf_file = Path(conf_dir).joinpath('config.ini')
    conf = read_config(conf_file)
    registry = ServiceRegistry.default()

    args, params = parse_args(registry, sys.argv[1:])

    reporter = _no_reporter if args.silent else _print_reporter


    reporter('Using configuration from %r', str(conf_file))

    try:
        params.validate()

        if args.gallery:
            base = Path(args.dst)
            base.mkdir(exist_ok=True)
            for style in registry.list():
                args.dst = base.joinpath(style + '.png')
                try:
                    _run(reporter, registry, conf, params,
                         args, dry_run=args.dry_run)
                except Exception as err:
                    # on error, continue with next service
                    reporter('ERROR for %r: %s', style, err)
        else:
            _run(reporter, registry, conf,
                 params, args, dry_run=args.dry_run)
    except Exception as err:
        reporter('ERROR: %s', err)
        raise
        return 1

    return 0


def parse_args(registry, argv):
    defaults = MapParams.default()
    parser = _setup_parser(registry, defaults)
    args = parser.parse_args(argv)

    params = defaults
    params.update(args.mapdef)
    params.update(args)

    return args, params


def _setup_parser(registry, defaults):
    parser = argparse.ArgumentParser(
        prog=APP_NAME,
        description=APP_DESC,
        epilog='{p} version {v} -- {author}'.format(
            p=APP_NAME,
            v=__version__,
            author=__author__,
        ),
    )

    parser.add_argument('--version',
                        action='version',
                        version=__version__,
                        help='Print version number and exit')

    parser.add_argument('mapdef',
                        metavar='MAPDEF',
                        action=MapParamsAction,
                        nargs='+',
                        help=('Map definition. Either two lat,lon'
                              ' pairs ("47.437,10.953 47.374,11.133")'
                              ' or a center point and a radius'
                              ' ("47.437,10.953 4km")'
                              ' or the path to an ini-file.'))

    default_dst = 'map.png'
    parser.add_argument('dst',
                        metavar='OUTPUT',
                        nargs='?',
                        default=default_dst,
                        help=('Where to save the generated image'
                              ' (default: %r).') % default_dst)

    def zoom(raw):
        v = int(raw)
        if v < MIN_ZOOM or v > MAX_ZOOM:
            raise ValueError(('Zoom value must be in interval'
                              ' %s..%s') % (MIN_ZOOM, MAX_ZOOM))
        return v

    parser.add_argument('-z', '--zoom',
                        type=zoom,
                        help=('Zoom level (%s..%s), higher means more detailed'
                              ' (default: %s).') % (MIN_ZOOM, MAX_ZOOM,
                                                    defaults.zoom))

    parser.add_argument('-s', '--style',
                        choices=registry.list(),
                        help='Map style (default: %r)' % defaults.style)

    parser.add_argument('-a', '--aspect',
                        type=parse.aspect,
                        help=(
                            'Aspect ratio (e.g. "16:9") for the generated map.'
                            ' Extends the bounding box to match the given'
                            ' aspect ratio.'))

    parser.add_argument('--copyright',
                        action='store_true',
                        help='Add copyright notice')

    parser.add_argument('--title',
                        action=TitleAction,
                        metavar='ARGS',
                        help=('Add a title to the map'
                              ' (optional args: PLACEMENT, COLOR, BORDER'
                              ' followed by title string)'))

    parser.add_argument('--comment',
                        action=CommentAction,
                        help='Add a comment to the map')

    parser.add_argument('--margin',
                        action=MarginAction,
                        help=('Add a margin (white space) around the map'
                              ' ("TOP RIGHT BOTTOM LEFT" or "ALL")'))

    parser.add_argument('--background',
                        type=parse.color,
                        metavar='RGBA',
                        help=('Background color for map margin'
                              ' (default: white)'))

    parser.add_argument('--frame',
                        action=FrameAction,
                        metavar='ARGS',
                        help=('Draw a frame around the map area'
                              ' (any of: WIDTH, COLOR, ALT_COLOR, STYLE and'
                              ' UNDERLAY)'))

    parser.add_argument('--scale',
                        action=ScaleAction,
                        metavar='ARGS',
                        help=('Draw a scale bar into the map'
                              ' (any of: PLACEMENT, WIDTH, COLOR, LABEL)'))

    # TODO: placement, color, outline, marker "N"
    parser.add_argument('--compass',
                        action='store_true',
                        help='Draw a compass rose on the map')

    parser.add_argument('--geojson',
                        nargs='+',
                        help=('Draw GeoJSON elements on the map.'
                              ' Path or JSON string'))

    parser.add_argument('--gallery',
                        action='store_true',
                        help=(
                            'Create a map image for each available style.'
                            ' WARNING: generates a lot of images.'))

    parser.add_argument('--dry-run',
                        action='store_true',
                        help='Show map info, do not download tiles')

    parser.add_argument('--no-cache',
                        action='store_true',
                        help='Do not use cached map tiles')

    parser.add_argument('--silent',
                        action='store_true',
                        help='Do not output messages to the console')

    return parser


def _run(report, registry, conf, params, args, dry_run=False):
    '''Build the tilemap, download tiles and create the image.'''
    p = params
    m = p.create_map()

    if dry_run:
        _show_info(report, p)
        return

    use_cache = not args.no_cache
    img = _build_map(m, p.style, p.zoom, use_cache, conf, registry, report)

    with open(args.dst, 'wb') as f:
        img.save(f, format='png')

    report('Map saved to %s', args.dst)


def _build_map(m, style, zoom, use_cache, conf, registry, report):
    service = registry.get(style)
    if use_cache:
        service = service.cached(limit=conf.cache_limit)

    return m.render(service,
                    zoom,
                    icons=icons.IconProvider(conf.icons_base),
                    parallel_downloads=8,
                    reporter=report)


def _print_reporter(msg, *args):
    print(msg % args)


def _no_reporter(msg, *args):
    pass


def _show_info(report, mapdef):
    bbox = mapdef.bbox
    area_w = int(distance(bbox.minlat, bbox.minlon, bbox.maxlat, bbox.minlon))
    area_h = int(distance(bbox.minlat, bbox.minlon, bbox.minlat, bbox.maxlon))
    unit = 'm'
    if area_w > 1000 or area_h > 1000:
        area_w = int(area_w / 100) / 10
        area_h = int(area_h / 100) / 10
        unit = 'km'

    report('-------------------------------')
    report('Area:        %s x %s %s', area_w, area_h, unit)
    report('Dimensions:  %s x %s px', area_w, area_h)
    report('Zoom Level:  %s', mapdef.zoom)
    report('Style:       %s', mapdef.style)
    report('-------------------------------')


def read_config(path):
    '''Read configuration from the given file in .ini format.
    Returns names and url patterns for services and API keys, combined from
    built-in configuration and the specified file.'''
    cfg = configparser.ConfigParser()

    # built-in defaults
    cfg.read_file(io.TextIOWrapper(resource_stream('mapmaker', 'default.ini')))

    # user settings
    cfg.read([path, ])

    parallel = cfg.getint('mapmaker', 'parallel_downloads', fallback=1)

    icons_base = cfg.get('icons', 'base', fallback=None)
    if icons_base:
        icons_base = Path(icons_base)
        # TODO: check is_abs, only join if relative
        data_dir = Path(appdirs.user_data_dir(appname=APP_NAME))
        icons_base = data_dir.joinpath(icons_base)

    return Config(copyrights={k: v for k, v in cfg.items('copyright')},
                  cache_limit=cfg.getint('cache', 'limit', fallback=None),
                  parallel_downloads=parallel,
                  icons_base=icons_base)


if __name__ == '__main__':
    sys.exit(main())
