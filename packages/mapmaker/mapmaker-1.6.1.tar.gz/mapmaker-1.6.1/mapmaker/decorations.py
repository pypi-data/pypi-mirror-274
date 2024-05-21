'''Decorations are graphic elements that are painted over and around the map
content, for example a title or a legend.

Decorations are placed using pixel coordinates.
'''


from math import ceil, floor

from . import geo
from .geo import decimal
from .geo import dms
from .render import contrast_color, load_font


# Placment locations on the MAP and MARGIN area.
PLACEMENTS = (
    'NW', 'NNW', 'N', 'NNE', 'NE',
    'WNW', 'W', 'WSW',
    'ENE', 'E', 'ESE',
    'SW', 'SSW', 'S', 'SSE', 'SE',
    'C',
)


class Decoration:
    '''Base class for decorations.

    Subclasses must implement the ``calc_size()`` and ``draw()`` methods.
    '''

    def __init__(self, placement):
        self.placement = placement
        self.margin = (4, 4, 4, 4)

    def calc_size(self, rc, map_size):
        '''Calculate the size of this decoration in pixels.
        ``rc`` is the "rendering context" which allows us to project lat/lon
        coordinates into pixel positions within the map.

        ``map_size`` is the size of the map content.
        '''
        raise ValueError('Not implemented')

    def draw(self, draw, rc, map_size):
        '''Draw this decoration using the given drawing context.

        ``draw`` is the drawing context.
        ``rc`` is the "rendering context" which allows us to project lat/lon
        coordinates into pixel positions within the map.
        ``map_size`` is the size of the map content.
        '''
        raise ValueError('Not implemented')


class Cartouche(Decoration):
    '''Draws a text area either on the map or on the margin.

    The text can have a box with an optional border or background color.

    :title:         The text content to be shown.
    :placement:     Where to place this decoration.
    :color:         The Text color as an RGBA tuple.
    :background:    The fill color for the text box as an RGBA tuple. Can be
                    *None* to omit the background.
    :border_width:  Width in pixels of the border line around the text box.
                    Can be ``0`` for no border.
    :border_color:  Color of the border line as an RGBA tuple.
    :font_name:     Name of the font in which the text should be drawn.
    :font_size:     Size of the label text.
    '''

    _MARGIN_MASK = {
        'NW': (1, 1, 1, 1),
        'NNW': (1, 1, 1, 0),
        'N': (1, 1, 1, 1),
        'NNE': (1, 0, 1, 1),
        'NE': (1, 1, 1, 1),
        'ENE': (0, 1, 1, 1),
        'E': (1, 1, 1, 1),
        'ESE': (1, 1, 0, 1),
        'SE': (1, 1, 1, 1),
        'SSE': (1, 0, 1, 1),
        'S': (1, 1, 1, 1),
        'SSW': (1, 1, 1, 0),
        'SW': (1, 1, 1, 1),
        'WSW': (1, 1, 0, 1),
        'W': (1, 1, 1, 1),
        'WNW': (0, 1, 1, 1),
    }

    # on the western and southern sides, rotate by 90^
    _ROTATION = {
        'NW': 0,
        'NNW': 0,
        'N': 0,
        'NNE': 0,
        'NE': 0,
        'ENE': 90,
        'E': 90,
        'ESE': 90,
        'SE': 0,
        'SSE': 0,
        'S': 0,
        'SSW': 0,
        'SW': 0,
        'WSW': 90,
        'W': 90,
        'WNW': 90,
    }

    # [horizontal][vertical]
    # horizontal:
    # - [l]eft
    # - [m]iddle  | ba[s]eline for vertical text
    # - [r]ight
    #
    # vertival:
    # - [t]op or [ascender]
    # - [m]iddle or ba[s]eline
    # - [b]ottom or [d]escender
    _TEXT_ANCHOR = {
        'NW': 'rd',
        'NNW': 'ld',
        'N': 'md',
        'NNE': 'rd',
        'NE': 'ld',
        'ENE': 'la',
        'E': 'lm',
        'ESE': 'ld',
        'SE': 'la',
        'SSE': 'ra',
        'S': 'ma',
        'SSW': 'la',
        'SW': 'ra',
        'WSW': 'rd',
        'W': 'rm',
        'WNW': 'ra',
    }

    # TODO: rename background => fill (see fill params in draw.py)
    # TODO: params for padding

    def __init__(self, title,
                 placement='N',
                 color=(0, 0, 0, 255),
                 background=None,
                 border_width=0,
                 border_color=None,
                 font_name=None,
                 font_size=12):
        '''Initialize a Text area.'''
        super().__init__(placement)
        self.title = title
        self.color = color
        self.background = background
        self.border_width = border_width or 0
        self.border_color = border_color
        self.font_name = font_name or 'DejaVuSans'
        self.font_size = font_size
        self.padding = (4, 8, 4, 8)  # padding between text and border

        # TODO: when placed at the edge, add 1px padding towards edge

    def calc_size(self, rc, map_size):
        if not self.title or not self.title.strip():
            return 0, 0

        font = load_font(self.font_name, self.font_size)

        left, top, right, bottom = font.getbbox(self.title,
                                                anchor=self._anchor)
        w = right - left
        h = bottom - top

        m_top, m_right, m_bottom, m_left = self.margin
        p_top, p_right, p_bottom, p_left = self.padding

        w += m_left + m_right + p_left + p_right
        h += m_top + m_bottom + p_top + p_bottom

        w += self.border_width * 2
        h += self.border_width * 2

        return w, h

    def draw(self, draw, rc, size):
        if not self.title or not self.title.strip():
            return

        w, h = size
        font = load_font(self.font_name, self.font_size)

        # adjust margins for proper alignment with frame
        # TODO: this belongs into calc_margin_pos
        mask = self._MARGIN_MASK[self.placement]
        masked_margins = [v * m for v, m in zip(self.margin, mask)]
        m_top, m_right, m_bottom, m_left = masked_margins
        p_top, p_right, p_bottom, p_left = self.padding

        # border/decoration
        if self.border_width:
            draw.rectangle([m_left, m_top, w - m_right - 1, h - m_bottom - 1],
                           fill=self.background,
                           outline=self.border_color or self.color,
                           width=self.border_width)

        # text
        x = {
            'l': 0 + p_left + m_left,
            'm': w // 2,
            's': w // 2,
            'r': w - p_right - m_right,
        }[self._anchor[0]]
        y = {
            't': 0 + p_top + m_top,
            'a': 0 + p_top + m_top,
            'm': h // 2,
            's': h // 2,
            'b': h - p_bottom - m_bottom,
            'd': h - p_bottom - m_bottom,
        }[self._anchor[1]]
        draw.text((x, y), self.title,
                  font=font,
                  anchor=self._anchor,
                  fill=self.color)

    @property
    def _anchor(self):
        return self._TEXT_ANCHOR[self.placement]

    def __repr__(self):
        return '<Cartouche placement=%r, title=%r>' % (self.placement,
                                                       self.title)


class Scale(Decoration):
    '''A scale bar that shows the size of the area on the map in meters or
    kilometers.

    :placement:     Where to place this decoration.
    :color:         The color for the scale and label as an RGBA tuple.
    :border_width:  Width in pixels for the lines of the scale bar.
    :underlay:      Draws a transparent background below the scale to improve
                    readability against the map content.
                    One of ``compact``, ``full`` (width), ``none``.
    :draw_label:    Whether to draw a label (*boolean*).
    :font_name:     Name of the font in which the label should be drawn.
    :font_size:     Size of the label text.
    '''

    LABEL_STYLES = ('default', 'nolabel')
    UNDERLAY_STYLES = ('compact', 'full', 'none')

    def __init__(self,
                 placement='SW',
                 color=(0, 0, 0, 255),
                 border_width=2,
                 underlay='compact',
                 label_style='default',
                 font_name=None,
                 font_size=10):
        super().__init__(placement)
        self.color = color
        self.border_width = border_width
        self.font_name = font_name or 'DejaVuSans'
        self.font_size = font_size

        if underlay not in Scale.UNDERLAY_STYLES:
            raise ValueError('Invalid underlay style %r' % underlay)
        self.underlay_style = underlay

        if label_style not in Scale.LABEL_STYLES:
            raise ValueError('Invalid label style %r' % label_style)
        self.label_style = label_style

        # TODO: might depend on placement?
        self._label_anchor = 'mt'  # centered, align-top

    def calc_size(self, rc, map_size):
        tick_size, tick_width, num_ticks = self._determine_tick(rc)

        m_top, m_right, m_bottom, m_left = self.margin

        # Size of the scale bar w/ ticks
        if self.underlay_style == 'full':
            map_width, _ = map_size
            w = map_width
        else:
            w = tick_width * num_ticks
            w += m_left + m_right

        h = self._tick_height()
        h += m_top + m_bottom

        # Size of the label
        if self._show_label:
            font = load_font(self.font_name, self.font_size)
            label = self._label(tick_size, num_ticks)
            left, top, right, bottom = font.getbbox(label,
                                                    anchor=self._label_anchor)
            label_h = bottom - top
            h += label_h + self._label_margin

        return (w, h)

    def draw(self, draw, rc, map_size):
        tick_size, tick_width, num_ticks = self._determine_tick(rc)
        w = tick_width * num_ticks

        if self.underlay_style != 'none':
            self._draw_underlay(draw, rc, map_size)

        self._draw_bar(draw, w, tick_width, num_ticks)

        if self._show_label:
            self._draw_label(draw, w, tick_size, num_ticks)

    def _draw_underlay(self, draw, rc, map_size):
        '''Draw a flat background in a light color with some opacity
        to improve the readability for the scale bar.'''
        w, h = self.calc_size(rc, map_size)
        p0 = (0, 0)
        p1 = None
        if self.underlay_style == 'compact':
            p1 = (w, h)
        elif self.underlay_style == 'full':
            map_width, _ = map_size
            p1 = (map_width, h)
        else:
            # should not happen
            raise RuntimeError('Bad underlay style: %r' % self.underlay_style)

        r, g, b, _ = contrast_color(self.color)
        alpha = 255 // 3
        draw.rectangle([p0, p1],
                       fill=(r, g, b, alpha),
                       width=0)

    def _draw_bar(self, draw, bar_width, tick_width, num_ticks):
        '''Draw the scale bar including ticks.'''
        tick_height = self._tick_height()
        m_top, m_right, m_bottom, m_left = self.margin

        # base line + outer ticks
        y = tick_height + m_top
        start = (m_left, y)
        end = (bar_width + m_left, y)

        # the "tips" of the start and end ticks
        start_tick = (m_left, m_top)
        end_tick = (bar_width + m_left, m_top)

        draw.line([start_tick, start, end, end_tick],
                  fill=self.color,
                  width=self.border_width,
                  joint='curve')

        # minor ticks
        y1 = tick_height + m_top
        for i in range(1, num_ticks):
            y0 = ceil(tick_height * 0.6)
            x = tick_width * i
            x += m_left
            draw.line([x, y0, x, y1],
                      fill=self.color,
                      width=self.border_width)

    def _draw_label(self, draw, bar_width, tick_size, num_ticks):
        '''Draw the label below the scale bar.'''
        tick_height = self._tick_height()
        m_top, _, _, m_left = self.margin
        x = bar_width // 2 + m_left
        y = m_top + tick_height + self._label_margin

        font = load_font(self.font_name, self.font_size)
        draw.text((x, y),
                  self._label(tick_size, num_ticks),
                  font=font,
                  anchor=self._label_anchor,
                  fill=self.color)

    def _determine_tick(self, rc):
        '''Determine the tick details:

        :tick_size: size of one tick in meters
        :tick_width: width of one tick mark in pixels
        :num_ticks: number of ticks that fit into the map
        '''
        # latitude at which distances are measured
        bbox = rc.bbox
        ref_lat = bbox.minlat
        # width of the map area in meters
        map_width = geo.distance(bbox.minlon,
                                 ref_lat,
                                 bbox.maxlon,
                                 ref_lat)

        tick_size = None    # in meters
        tick_count = None
        tick_area = 10  # "n" to use ca. 1/n of the map
        max_tick_count = 5 * tick_area

        # if a tick was "s" meters wide, how many would fit on the map?
        # "s" from 10,000 to 0.5
        for e in range(14, 0, -1):
            s = 10 ** e / 2
            c = floor(map_width / s)
            if c > max_tick_count:
                break
            tick_size = s
            tick_count = c

        if not (tick_size and tick_count):
            return (0, 0, 0)

        # tick_count tells how many full ticks fit into the complete map width
        # but we only want to fill part of the view.
        num_ticks = ceil(tick_count / tick_area)

        # How wide is a tick in pixels?
        lon0 = bbox.minlon
        _, lon1 = geo.destination_point(ref_lat, lon0, geo.BRG_EAST, tick_size)

        x0, _ = rc.to_pixels(ref_lat, lon0)
        x1, _ = rc.to_pixels(ref_lat, lon1)
        tick_width = x1 - x0

        return tick_size, tick_width, num_ticks

    def _label(self, tick_size, num_ticks):
        scale_width = tick_size * num_ticks
        unit = 'km' if scale_width >= 1_000 else 'm'
        value = scale_width / 1_000 if scale_width >= 1_000 else scale_width
        return '{0:,.0f} {1}'.format(value, unit)

    @property
    def _show_label(self):
        return self.label_style != 'nolabel'

    @property
    def _label_margin(self):
        '''Margin between label and scale bar.'''
        return max(self.font_size // 2, 4)

    def _tick_height(self):
        return 10


class CompassRose(Decoration):
    '''Draws a compass rose at the given placement location on the map.

    The "compass" consists of an error pointing north
    and an optional "N" marker at the top of the arrow.

    :placement: Where to place the compass rose (usually in the map area).
    :color:     Main (fill) color for the compass rose. RGBA tuple.
    :outline:   Optional outline for the shape.
    :marker:    Whether to include a "N" marker at the northern tip (boolean).
    '''

    def __init__(self,
                 placement='SE',
                 color=(0, 0, 0, 255),
                 outline=None,
                 marker=False):
        super().__init__(placement)
        self.color = color
        self.outline = outline
        self.marker = marker

        self.font = 'DejaVuSans.ttf'  # for Marker ("N")
        self.margin = (12, 12, 12, 12)

    def calc_size(self, rc, map_size):
        map_w, map_h = map_size
        w = int(map_w * 0.05)
        h = int(map_h * 0.1)

        m_top, m_right, m_bottom, m_left = self.margin
        w += m_left + m_right
        h += m_top + m_bottom

        return w, h

    def draw(self, draw, rc, size):
        # basic arrow
        #        a
        #       /\
        #     /   \
        #   /      \    <-- head
        # b ---  --- c
        #    d| |e
        #     | |       <- tail
        #     |_|
        #   f  i  g
        w, h = size
        m_top, m_right, m_bottom, m_left = self.margin
        w -= m_left + m_right
        h -= m_top + m_bottom

        # subtract vertical space for "N" marker
        font = None
        marker_pad = 0
        marker_h = 0
        if self.marker:
            font = load_font(self.font, self.font_size)
            marker_w, marker_h = font.getsize('N')
            marker_pad = marker_h // 16  # padding between marker and arrowhead
            h -= marker_h
            h -= marker_pad

        head_h = h // 2.2
        tail_h = h - head_h
        tail_w = w // 4

        ax = w // 2
        ay = 0

        bx = 0
        by = head_h
        by += (head_h // 4)  # pull down the outer points of the arrow
        cx = w
        cy = by

        dx = w // 2 - tail_w // 2
        dy = head_h
        ex = w // 2 + tail_w // 2
        ey = head_h

        fx = tail_w
        fx -= tail_w // 6  # make the base of the tail a bit wider
        fy = h
        gx = w - tail_w
        gx += tail_w // 6  # make the base of the tail a bit wider
        gy = fy

        ix = w // 2
        iy = h
        iy -= tail_h // 3  # pull base line inwards

        points = [
            (ax, ay),
            (cx, cy),
            (ex, ey),
            (gx, gy),
            (ix, iy),
            (fx, fy),
            (dx, dy),
            (bx, by),
        ]
        x_offset = m_left
        y_offset = m_top + marker_h + marker_pad
        draw.polygon([(x + x_offset, y + y_offset) for x, y in points],
                     fill=self.color,
                     outline=self.outline)

        if self.marker:
            w, h = size
            x = w // 2
            y = m_top
            draw.text((x, y), 'N',
                      font=font,
                      anchor='mt',
                      fill=self.color,
                      stroke_width=1,
                      stroke_fill=self.outline)

    def __repr__(self):
        return '<CompassRose placement=%r>' % self.placement


class Frame:
    '''Draws a frame around the map content.

    Either a "solid" border or a two-colored border sized according to lat/lon
    coordinates.

    The frame width adds to the total size of the map image.

    :width:         The width in pxiels.
    :color:         The primary color of the frame. RGBA tuple.
    :alt_color:     The secondary ("alternating") color for two-colored style.
    :style:         Either ``solid`` or ``coordinates``.
    '''

    STYLES = ('coordinates', 'solid')

    def __init__(self,
                 width=8,
                 color=(0, 0, 0, 255),
                 alt_color=(255, 255, 255, 255),
                 style='solid'):
        self.width = width
        self.color = color
        self.alt_color = alt_color
        self.style = style

    def draw(self, rc, draw, size):
        if self.style == 'coordinates':
            self._draw_coords(rc, draw, size)
        else:
            self._draw_solid(rc, draw, size)

    def _draw_solid(self, rc, draw, size):
        # bottom right pixel for rectangle is *just outside* xy
        w, h = size
        xy = (0, 0, w - 1, h - 1)
        draw.rectangle(xy, outline=self.color, width=self.width)

    def _draw_coords(self, rc, draw, size):
        crop_left, crop_top, _, _ = rc.crop_box
        _, h = size

        top, right, bottom, left = self._tick_coordinates(rc.bbox)
        for which, coords in enumerate((top, bottom)):
            prev_x = self.width
            for i, tick_pos in enumerate(coords):
                # x, y are pixels on the MAP
                # draw context refers to the size incl. border around the map
                x, y = rc.to_pixels(*tick_pos)
                x -= crop_left
                x += self.width

                y -= crop_top
                if which == 1:  # bottom
                    y += self.width

                # "-1" accounts for 1px border
                draw.rectangle([
                    prev_x, y,
                    x - 1, y + self.width - 1],
                    fill=self.color if i % 2 else self.alt_color,
                    outline=self.color,
                    width=1
                )
                prev_x = x

        for which, coords in enumerate((left, right)):
            prev_y = self.width
            prev_y = h - self.width - 1
            for i, tick_pos in enumerate(coords):
                x, y = rc.to_pixels(*tick_pos)

                x -= crop_left
                if which == 1:  # right
                    x += self.width

                y -= crop_top
                y += self.width

                xy = [x,
                      y - 1,
                      x + self.width - 1,
                      prev_y]
                fill = self.color if i % 2 else self.alt_color
                draw.rectangle(xy,
                               fill=fill,
                               outline=self.color,
                               width=1)
                prev_y = y

        self._draw_corners(draw, size)

    def _tick_coordinates(self, bbox, n=5):
        # regular ticks
        lon_ticks = self._ticks(bbox.minlon, bbox.maxlon, n)
        # partial tick for the last segment
        lon_ticks.append(bbox.maxlon)

        lat_ticks = self._ticks(bbox.minlat, bbox.maxlat, n)
        lat_ticks.append(bbox.maxlat)

        top = [(bbox.maxlat, lon) for lon in lon_ticks]
        bottom = [(bbox.minlat, lon) for lon in lon_ticks]
        left = [(lat, bbox.minlon) for lat in lat_ticks]
        right = [(lat, bbox.maxlon) for lat in lat_ticks]

        return top, right, bottom, left

    def _ticks(self, start, end, n):
        '''Create a list of ticks from start to end so that we have ``n`` ticks
        in total (plus a fraction) and the tick values are on full degrees,
        minutes or seconds if possible.
        '''
        span = end - start
        d, m, s = dms(span)
        m_half = m * 2

        steps = []
        if d >= n:
            per_tick = d // n
            n_ticks = floor(span / decimal(d=per_tick))
            steps = [decimal(d=i * per_tick) for i in range(1, n_ticks + 1)]
        elif m >= n:
            per_tick = m // n
            n_ticks = floor(span / decimal(m=per_tick))
            steps = [decimal(m=i * per_tick) for i in range(1, n_ticks + 1)]
        elif m_half >= n:
            per_tick = (m_half // n) / 2
            n_ticks = floor(span / decimal(m=per_tick))
            steps = [decimal(m=i * per_tick) for i in range(1, n_ticks + 1)]
        else:
            per_tick = s // n
            n_ticks = floor(span / decimal(s=per_tick))
            steps = [decimal(s=i * per_tick) for i in range(1, n_ticks + 1)]

        ticks = [start + v for v in steps]
        return ticks

    def _draw_corners(self, draw, size):
        w, h = size
        width = self.width
        draw.rectangle([0, 0, width - 1, width - 1], fill=self.color)
        draw.rectangle([w - width, 0, w - 1, width - 1], fill=self.color)
        draw.rectangle([0, h - width, width - 1, h - 1], fill=self.color)
        draw.rectangle([w - width, h - width, w - 1, h - 1], fill=self.color)

    def __repr__(self):
        return '<Frame width=%r, style=%r>' % (self.width, self.style)
