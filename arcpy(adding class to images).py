import arcpy
import os

raster_path = r"C:\\Users\\wassef\\Documents\\ArcGIS\\Projects\\Mywork\\Modis_image_dataset\\MCD12Q1.A2012.hdf.tif"

# Check if the file exists
if not os.path.exists(raster_path):
    print(f"Error: The file at {raster_path} does not exist.")
else:
    print("File exists, proceeding to create the raster layer...")
# The name of the raster layer as it appears in the Table of Contents
raster_layer_name = "MCD12Q1.A2002.hdf.tif"
# Replace with the exact layer name

# Get the current project and map
aprx = arcpy.mp.ArcGISProject("CURRENT")
map = aprx.listMaps()[0]  # Assuming you want the first map in the project

# Find the raster layer in the map
layer = None
for lyr in map.listLayers():
    if lyr.name == raster_layer_name:
        layer = lyr
        break

# Initialize the list to store class values
class_values = []

if layer:
    try:
        # Get the path of the raster dataset
        raster_path = layer.dataSource
        
        # Iterate through the raster attribute table
        with arcpy.da.SearchCursor(raster_path, ["Classe"]) as cursor:
            for row in cursor:
                class_value = row[0]
                class_values.append(class_value)  # Correctly appending to the list
        
        print("Class values extracted:", class_values)
        
    except Exception as e:
        print(f"Error accessing raster layer: {e}")
else:
    print(f"Layer {raster_layer_name} not found in the map.")

# The names of the raster layers as they appear in the Table of Contents
raster_layer_names = ["MCD12Q1.A2012..hdf.tif", "MCD12Q1.A2022.hdf.tif"]  # Replace with your layer names
raster_layer_names = ["LandCover_2017"]
# List of class va"Sentinal-2 _image_dataset\\LandCover_2017"lues to fill in the new column (make sure this list is long enough for both layers) # 

# Get the current project and map
aprx = arcpy.mp.ArcGISProject("CURRENT")
map = aprx.listMaps()[0]  # Assuming you want the first map in the project

for raster_layer_name in raster_layer_names:
    # Find the raster layer in the map
    layer = None
    for lyr in map.listLayers():
        if lyr.name == raster_layer_name:
            layer = lyr
            break

    if layer:
        try:
            # Get the path of the raster dataset
            raster_path = layer.dataSource
            
            # Field name to update
            field_name = "Class"

            # Check if the field already exists
            fields = [f.name for f in arcpy.ListFields(raster_path)]
            if field_name not in fields:
                print(f"Field '{field_name}' does not exist in {raster_layer_name}. Adding the field.")
                arcpy.management.AddField(raster_path, field_name, "Text")  # Use appropriate field type

            # Update the new field with values from the list
            with arcpy.da.UpdateCursor(raster_path, [field_name]) as cursor:
                for i, row in enumerate(cursor):
                    if i < len(class_values):
                        row[0] = class_values[i]
                        cursor.updateRow(row)
                    else:
                        break  # Exit if there are more rows than values

            print(f"Field '{field_name}' in {raster_layer_name} updated with values from class_values.")
            
        except Exception as e:
            print(f"Error updating raster field in {raster_layer_name}: {e}")
    else:
        print(f"Layer {raster_layer_name} not found in the map.")
