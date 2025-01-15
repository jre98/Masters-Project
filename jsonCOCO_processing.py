import json
import os
import cv2
from detectron2.structures import BoxMode

# This function converts image label (partially) to the expected detectron2 format
def convert_imglabel_to_detectron2(json_file):
    # Open the current label file passed to the function and get the data
    with open(json_file) as f:
        data = json.load(f)

    dataset_dicts = []
    for idx, shape in enumerate(data["shapes"]):
        record = {}
        # Pull relevant data about the image and store in the "record" dictionary
        record["file_name"] = data["imagePath"]
        record["image_id"] = idx
        record["height"] = data["imageHeight"]
        record["width"] = data["imageWidth"]
        # Find the min and max x and y values of the shape drawn in LabelMe
        # These values will be used to fill out the bbox field
        min_x = min(x[0] for x in shape["points"])
        min_y = min(x[1] for x in shape["points"])
        max_x = max(x[0] for x in shape["points"])
        max_y = max(x[1] for x in shape["points"])

        # These values will be used to assign the values in the bbox field
        x = min_x
        y = min_y
        width = max_x - min_x
        height = max_y - min_y
        # Create an object that will be saved to the json file
        obj = {
            # Assign the values of the bbox field to their correct place
            "bbox": [x,
                     y,
                     width,
                     height],
            # Set bbox mode to 1 so that the bbox coordinates are interpreted correctly
            "bbox_mode": 1,
            # Passes the polygon points as the segmentation points
            "segmentation": [shape["points"]],
            # Use 0 for the category, as there is only one type of object being detected
            "category_id": 0,  
            
        }
        record["annotations"] = [obj]
        dataset_dicts.append(record)
    return dataset_dicts


# First, we need to loop through each file in the folder
# Path to the folder containing the JSON files
folder_path = "/Users/jacob/Desktop/CPSC 597/detectron items/jsonConversion/Pre Conversion"

# This string is used to add on to the filename of the saved json file to distinguish it from the original file
s = "TMP"
# Loop through each file in the specified folder
for filename in os.listdir(folder_path):
    # Check if the file is a JSON file
    if filename.endswith('.json'):
        print("Beginning processing file: ", filename, "\n")
        # If it is, construct the full path to the JSON file
        file_path = os.path.join(folder_path, filename)
        
        # Call helper function to do some of the formatting
        dataset_dicts = convert_imglabel_to_detectron2(file_path)

        new_file_name = s + filename
        # Save the converted annotations to a new json file
        output_path = "/Users/jacob/Desktop/CPSC 597/detectron items/jsonConversion/Post Conversion/"
        output_path += new_file_name

        print("The file will be saved at the following location and the following name", output_path, "\n")
        
        with open(output_path, "w") as f:
            json.dump(dataset_dicts, f)
        
        print("Finished processing file: ", filename, "\n")

