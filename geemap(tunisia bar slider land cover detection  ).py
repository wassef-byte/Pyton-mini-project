
# Define the region of interest (Tunisia)
tunisia = ee.FeatureCollection("FAO/GAUL/2015/level0").filter(ee.Filter.eq('ADM0_NAME', 'Tunisia'))

def esri_annual_land_cover(year):
    collection = ee.ImageCollection(
        'projects/sat-io/open-datasets/landcover/ESRI_Global-LULC_10m_TS'
    )
    start_date = ee.Date.fromYMD(year, 1, 1)
    end_date = start_date.advance(1, 'year')
    image = collection.filterDate(start_date, end_date).mosaic()
    return image.set('system:time_start', start_date.millis())

start_year = 2017
end_year = 2023
years = ee.List.sequence(start_year, end_year)
images = ee.ImageCollection(years.map(esri_annual_land_cover))
# Clip the image collection to Tunisia
clipped_collection = images.map(lambda image: image.clip(tunisia))
# Create a map centered on Tunisia with zoom level 9
Map = geemap.Map(center=[34.0, 9.0], zoom=9)

palette = [
    "#1A5BAB",
    "#358221",
    "#000000",
    "#87D19E",
    "#FFDB5C",
    "#000000",
    "#ED022A",
    "#EDE9E4",
    "#F2FAFF",
    "#C8C8C8",
    "#C6AD8D",
]
vis_params = {"min": 1, "max": 11, "palette": palette}

Map = geemap.Map()
Map.ts_inspector(clipped_collection, left_vis=vis_params, date_format='YYYY')
Map.add_legend(title="Esri Land Cover", builtin_legend='ESRI_LandCover')
Map