import ee
import geemap

ee.Authenticate()
credentials = ee.ServiceAccountCredentials(
    key_file = r'C:\your api code ',
    email = "you email"
)
ee.Initialize(credentials=credentials)
Map = geemap.Map()
roi = Map.user_roi

# Function to filter image collections
def filter_col(col, roi, date):
    return col.filterDate(date[0], date[1]).filterBounds(roi)

# Function to create composite for Landsat 4, 5, and 7
def landsat457(roi, date):
    col = (filter_col(ee.ImageCollection('LANDSAT/LT04/C02/T1_L2'), roi, date)
           .merge(filter_col(ee.ImageCollection('LANDSAT/LT05/C02/T1_L2'), roi, date))
           .merge(filter_col(ee.ImageCollection('LANDSAT/LE07/C02/T1_L2'), roi, date)))
    image = col.map(cloud_mask_tm).median().clip(roi)
    return image

# Function to create composite for Landsat 8 and 9
def landsat89(roi, date):
    col = (filter_col(ee.ImageCollection('LANDSAT/LC08/C02/T1_L2'), roi, date)
           .merge(filter_col(ee.ImageCollection('LANDSAT/LC09/C02/T1_L2'), roi, date)))
    image = col.map(cloud_mask_oli).median().clip(roi)
    return image

# Cloud mask function for Landsat 4, 5, and 7
def cloud_mask_tm(image):
    qa = image.select('QA_PIXEL')
    dilated = 1 << 1
    cloud = 1 << 3
    shadow = 1 << 4
    mask = (qa.bitwiseAnd(dilated).eq(0)
            .And(qa.bitwiseAnd(cloud).eq(0))
            .And(qa.bitwiseAnd(shadow).eq(0)))
    
    return image.select(['SR_B1', 'SR_B2', 'SR_B3', 'SR_B4', 'SR_B5', 'SR_B7'], ['B2', 'B3', 'B4', 'B5', 'B6', 'B7']).updateMask(mask)

# Cloud mask function for Landsat 8 and 9
def cloud_mask_oli(image):
    qa = image.select('QA_PIXEL')
    dilated = 1 << 1
    cirrus = 1 << 2
    cloud = 1 << 3
    shadow = 1 << 4
    mask = (qa.bitwiseAnd(dilated).eq(0)
            .And(qa.bitwiseAnd(cirrus).eq(0))
            .And(qa.bitwiseAnd(cloud).eq(0))
            .And(qa.bitwiseAnd(shadow).eq(0)))
    
    return image.select(['SR_B2', 'SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'], ['B2', 'B3', 'B4', 'B5', 'B6', 'B7']).updateMask(mask)

years = [1990, 2000, 2010]


# Generate image composites and visualize the
for year in years:
    def landsat_annual_land_cover(year):
        year = ee.Number(year)

        # Determine which function to use based on the year
        landsat_fn = ee.Algorithms.If(year.lt(2014), landsat457, landsat89)

        start = ee.Date.fromYMD(year.subtract(1).int(), 1, 1)
        end = ee.Date.fromYMD(year.add(1).int(), 12, 31)

        date_range = [start, end]

        # Create the image composite
        image = ee.Image(ee.Algorithms.If(year.lt(2014),
                                          landsat457(roi, date_range),
                                          landsat89(roi, date_range)
                                         )).multiply(0.0000275).add(-0.2)

        rgb_image = image.select(['B4', 'B3', 'B2'])


        return Map.addLayer(Landsat_img, 
                            {'bands': ['B4', 'B3', 'B2'], 'min': 0.07928948633916319, 
                             'max': 0.1951775968839408,
                             'opacity': 1.0, 
                             'gamma': 1.4}
        , f'Landsat Img  {year}')
for year in years:
    landsat_annual_land_cover(year)
# Add layer control to the map
Map.add_layer_control()

# Display the map
Map    
    