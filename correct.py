'''
You can get into you manage.py shell after running world.load.run()

Run::

    >>> from world.correct import run
    >>> run()

'''

def run():
    import os
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

    from psycopg2 import IntegrityError
    from django.contrib.gis.utils import mapping, LayerMapping, add_postgis_srs

    from world.models import WorldBorders

    try:
        add_postgis_srs(900913)
    except IntegrityError:
        print "The Google Spherical Mercator projection, or a projection with srid 900913, already exists, skipping insert"

    WORLD_SHP = 'apps/world/data/TM_WORLD_BORDERS-0.3.shp'
    layer = LayerMapping(WorldBorders,
                          WORLD_SHP,
                          mapping(WORLD_SHP,geom_name='mpoly',multi_geom=True),
                          transform=False,
                          encoding='iso-8859-1')

    layer.save(verbose=True,strict=True,progress=True)


    print 'Fixing invalid polygons...'
    num = len(WorldBorders.objects.extra(where=['NOT ST_IsValid(mpoly)']))
    for item in WorldBorders.objects.extra(where=['NOT ST_IsValid(mpoly)']):
        corrected = item.mpoly.buffer(0)
        item.mpoly = corrected
        item.save()

    print '....'
    num = len(WorldBorders.objects.extra(where=['NOT ST_IsValid(mpoly)']))
    if num:
      print '%s invalid polygons remain' % num
      print WorldBorders.objects.extra(where=['NOT ST_IsValid(mpoly)'])
