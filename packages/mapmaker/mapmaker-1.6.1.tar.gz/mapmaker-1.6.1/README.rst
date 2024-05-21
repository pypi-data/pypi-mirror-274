Map Maker
#########
``mapmaker`` is a simple script to generate map images for "Slippy Tile" maps.
Map tiles are downloaded from services such as OpenStreetMap and are combined
into a single image.


Installation
============
Use the installation script:

.. code:: shell-session

    $ python setup.py install

Or install using pip:

.. code:: shell-session

    $ pip install mapmaker


Command Line Usage
==================
Use ``mapmaker --help`` to show a detailed list of options.


Basic Usage
-----------
This will create a file ``map.png`` in the current directory. The map will
cover the bounding box specified with two pairs of lat/lon coordinates:

.. code:: shell-session

    $ mapmaker  47.44,10.95 47.37,11.13

One can also specify a center point and a radius:

.. code:: shell-session

    $ mapmaker 63.0695,-151.0074 100km

If the coordinates start with a negative value, use ``--`` to indicate the
end of command line flags:

.. code:: shell-session

    $ mapmaker -- -32.653197,-70.0112 100km

Coordinates can also be specified in DMS format:

.. code:: shell-session

    $ mapmaker "63°4'10.2'' N, 151°0'26.64'' W" 4km

Use a single quote for minutes (``'``)
and two single quotes (``''``) for seconds.
Note the quotes around the command line argument.


You can also specify the **output file** (default is *map.png*):

.. code:: shell-session

    $ mapmaker 63.0695,-151.0074 100km denali.png


Additional Options
------------------
Specify the **zoom level** with the ``--zoom`` flag. The default is 8.
Higher values mean more detail and result in larger map images.

.. code:: shell-session

    $ mapmaker 63.0695,-151.0074 100km --zoom 12

Use ``--style`` to control the **look** of the map:

.. code:: shell-session

    $ mapmaker 63.0695,-151.0074 100km --style human

To control the resulting image format, use ``--aspect``:

.. code:: shell-session

    $ mapmaker 45.83,6.88 100km --aspect 16:9

The aspect ratio is given in the format ``W:H`` (e.g. 4:3 or 19:9).
The resulting map image will contain the given bounding box (or point w/ radius)
and max be extended to North/South or East/West to match the aspect ratio.
Note that the *resolution* of the image depends on the ``--zoom`` factor.


Decorations
-----------
Set a headline with ``--title``, specify optional ``PLACEMENT``, ``COLOR``
and ``BORDER`` followed by the title string.
The title will be added to the *Margin Area* and will force a margin that is
large enough to accommodate the title.

:PLACEMENT:   one of the cardinal directions e.g. ``NW, NNW, N, NNE, NE, ...``.
:BORDER:      a single integer value for the border width in in pixels.
:COLOR:       RGB(A) tuple as a comma separated string, e.g. "255,0,0".
:BACKGROUND:  RGB(A) tuple as a comma separated string, e.g. "255,0,0".

Colors can also be specified as hex values, e.g. ``#ff0000``
or ``#ff000080`` (with opacity).

.. code:: shell-session

    $ mapmaker 45.83,6.88 100km --title My Map
    $ mapmaker 45.83,6.88 100km --title NNW My Map
    $ mapmaker 45.83,6.88 100km --title NNW 5 My Map
    $ mapmaker 45.83,6.88 100km --title NNW 5 255,0,0 My Map
    $ mapmaker 45.83,6.88 100km --title NNW 5 255,0,0 0,0,255 My Map

Use ``--comment`` to add a comment in small print. Arguments are the same
as for ``--title``:

.. code:: shell-session

    $ mapmaker 45.83,6.88 100km --comment My Comment
    $ mapmaker 45.83,6.88 100km --comment SE 200,200,200 My Comment

Use ``--margin`` and ``--background`` to apply a border around the map.
Note that some decoration arguments will automatically add a margin area.

``margin`` is given in pixels as a single value (all sides),
a pair of two values (top/bottom and left/right)
or as four separate values for top, right, bottom, left (clockwise).

.. code:: shell-session

    $ mapmaker 45.83,6.88 100km --margin 50
    $ mapmaker 45.83,6.88 100km --margin 20 40
    $ mapmaker 45.83,6.88 100km --margin 10 15 20 15

The color of the margin area can be controlled with ``--background``.
``background`` is given as a comma separated RGB(A) value:

.. code:: shell-session

    $ mapmaker 45.83,6.88 100km --margin 10 --background 200,200,200
    $ mapmaker 45.83,6.88 100km --margin 10 --background 200,200,200,128

The ``--frame`` argument adds a border around the map content, that is between
the map and the (optional) margin area.
``frame`` has up to four optional parameters:

:``WIDTH``:     The width in pixels, e.g. "8".
:``COLOR``:     The main color as an RGB(A) value, e.g. "0,0,0" (black).
:``ALT_COLOR``: The secondary color as an RGB(A) value, e.g. "255,255,255" (white).
:``STYLE``:     The style, either "solid" or "coordinates".

Arguments can be supplied in any order.
``ALT_COLOR`` is only needed for styles that feature alternating colors,
if two RGB(A) values are specified, the second is considered the ``ALT_COLOR``.

All arguments are optional and if ``--frame`` is specified without arguments,
a default frame will be drawn.

Examples:

.. code:: shell-session

    $ mapmaker 45.83,6.88 100km --frame
    $ mapmaker 45.83,6.88 100km --frame 12
    $ mapmaker 45.83,6.88 100km --frame 12 255,0,0
    $ mapmaker 45.83,6.88 100km --frame 12 255,0,0 0,0,255 coordinates
    $ mapmaker 45.83,6.88 100km --frame coordinates

Use ``--scale`` to show a scale bar on the map.
Optional arguments for scale are:

:``PLACEMENT``: Where to place the scale, must be one of the map areas
                (e.g "SW").
:``WIDTH``:     The width of the scale bar in pixels (e.g. "2").
:``COLOR``:     The color to use for the scale bar an label, e.g. "0,0,0".
:``LABEL``:     The label style, either ``default`` or ``nolabel``.
:``UNDERLAY``:  Draw a partly transparent box below the scale bar to improve
                its readability against the map content.

The label shows the size of the scale in meters or kilometers.

Examples:

.. code:: shell-session

    $ mapmaker 45.83,6.88 100km --scale
    $ mapmaker 45.83,6.88 100km --scale SE
    $ mapmaker 45.83,6.88 100km --scale 1
    $ mapmaker 45.83,6.88 100km --scale 120,120,120
    $ mapmaker 45.83,6.88 100km --scale nolabel
    $ mapmaker 45.83,6.88 100km --scale full
    $ mapmaker 45.83,6.88 100km --scale SE 1 120,120,120 nolabel full


GeoJSON
-------
The ``--geojson`` option can be used to draw `GeoJSON <https://geojson.org/>`_
objects onto the map.

The GeoJSON can contain additional attributes to control the color, line width,
etc. The additional attributes can be part of a *Geometry* or part of the
``properties`` attribute of a parent *Feature*.
Have a look hat the module documentation to see which special attributes are
supported.

.. code:: json

    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [12.594474, 55.691438]
      },
      "properties": {
        "symbol": "square",
        "color": [10, 147, 150],
        "size": 12
      }
    }

You can also use any *Geometry* object directly:

.. code:: json

    {
      "type": "Polygon",
      "coordinates": [
        [8.612316, 47.680632],
        [8.612316, 47.676327],
        [8.617423, 47.676327],
        [8.617423, 47.680632]
      ]
      "color": [60, 9, 108],
      "fill": [60, 9, 108, 120]
    }

The ``--geojson`` option supports a path to a JSON file or a JSON formatted
string.


Create a Gallery
----------------
Use the ``--gallery`` flag to render a set of maps, one for each available style.
In this case, you specify an output directory instead of a file (default is the
current directory).
This flag ignores the ``--style`` parameter.


Configuration
#############
The configuration file is located at ``~/.config/mapmaker/config.ini``


Styles (Tile Servers)
=====================
You can specify additional map styles like this:

.. code:: ini

    # ~/.config/mapmaker/config.ini

    [service.osm]
    osm   = https://tile.openstreetmap.org/{z}/{x}/{y}.png

    [service.opentopo]
    subdomains = abc
    topo       = https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png

Where ``osm`` or ``topo`` are the names of the style (as used in the
``--style`` flag) and the URL is the URL pattern for downloading tiles.

Section names can be chosen freely but have to start with ``service.``.
Each section may contain the following reserved entries:

.. code:: ini

    [service.example]
    tile_size  = 512
    api_key    = my-secret-api-key
    subdomains = abcdef

Any other entries are expected to be key/value pairs with URL patterns.
If no ``tile_size`` is configured, the default size (``256px``) is used.

The URL pattern **must** contain three variables:

:z: zoom level
:x: X-coordinate of the tile
:y: Y-coordinate of the tile

See for example https://wiki.openstreetmap.org/wiki/Tiles.

The URL may contain additional placeholders for an API Key (see below)
and a subdomain::

    topo        = https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png
                          ^^^
    atlas = https://tile.thunderforest.com/atlas/{z}/{x}/{y}.png?apikey={api}
                                                                         ^^^


Authorization
=============
Authorization is needed for the following services:

======================= ======= ======================================
Domain                  Type    Homepage
======================= ======= ======================================
tile.thunderforest.com  API Key https://www.thunderforest.com/
maps.geoapify.com       API Key https://www.geoapify.com/
api.mapbox.com          Token   https://mapbox.com/
======================= ======= ======================================

Most services offer a free plan for limited/non-commercial use. Check out the
URL from the table above.

Once you have registered, place your API Keys in a config file like this:

.. code:: ini

    # ~/.config/mapmaker/config.ini

    [service.thunderforest]
    api_key = YOUR_API_KEY

    [service.geoapify]
    api_key = YOUR_API_KEY

    [service.mapbox]
    api_key = YOUR_API_KEY

Where ``[service.xxx]`` is the config section which defines the URLs for this
service.
