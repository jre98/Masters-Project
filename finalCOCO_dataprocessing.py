import json
import os

# Basic helper function to write the formatted data to a text file
def write_to_file(filepath, content):
    with open(filepath, 'w') as f:
        f.write(content)

# This helper function extracts the important pieces of data from 
# the .json file currently being read
def extract_segmentation_and_bbox(json_file_path):
    # Open the file at the specified filepath and load the data
    with open(json_file_path, 'r') as f:
        data = json.load(f)

    # List to store the values we extract from the file
    extracted_values = []
    for item in data:
        file_name = item['file_name']
        for annotation in item['annotations']:
            bbox = annotation['bbox']
            # Convert list to comma-separated string for COCOjson format
            segmentation = ','.join(map(str, annotation['segmentation'][0]))  
            # Add all extracted values to the list to be returned
            extracted_values.append((bbox, segmentation, file_name))

    return extracted_values

# This helper function formats the segmentation portion properly, and then calculates
# the area of the polygon represented by the segmentation points
def polygonarea_and_segmentationformat(input_string):
    # Remove whitespace and newlines
    cleaned_string = input_string.strip().strip('[]').replace('\n', '').replace(' ', '')

    # Split the string into individual values (extract each set of points)
    values = cleaned_string.split('],[')

    # This will store the finalized segmentation data
    segmentation = []
    # Loop through each individual point in the segmentation array
    for val in values:
        # Currently, the points are formatted like
        x, y = val.split(',')
        segmentation.extend([float(x.strip('[')), float(y.strip(']'))])

    # Check if the segmentation has 8 points (4 pairs)
    if len(segmentation) != 8:
        raise ValueError("Segmentation must have 8 points (4 pairs)")

    # Extract x and y coordinates from the segmentation points
    x_coordinates = segmentation[::2]
    y_coordinates = segmentation[1::2]

    # Apply the Shoelace formula to calculate the area
    n = len(x_coordinates)
    area = 0
    for i in range(n):
        j = (i + 1) % n
        area += x_coordinates[i] * y_coordinates[j]
        area -= x_coordinates[j] * y_coordinates[i]
    area = abs(area) / 2

    return area, segmentation


# Folder path - want to loop through each .json file in this folder
folder_path = '/Users/jacob/Desktop/CPSC 597/detectron items/jsonConversion/Post Conversion'

# Loop through each file in the above folder path using the os library
for filename in os.listdir(folder_path):
    # This is used to track the number of annotations there are per .json file
    curr_annotation_num = 1
    # Check to make sure the current file is a .json file to make sure we don't read a different kind of file
    if filename.endswith('.json'):
        print("Processing file:", filename)
        # Assemble the full filepath of the current .json file
        curr_filepath = os.path.join(folder_path, filename)
        # Use the helper funtion to extract the segmentation and 
        values = extract_segmentation_and_bbox(curr_filepath)
        output_filepath = '/Users/jacob/Desktop/CPSC 597/detectron items/jsonConversion/COCO Format/' + filename + '_output.txt'
        # output_filepath = os.path.splitext(curr_filepath)[0] + '_output.txt'
        output_content = ""
        for bbox, segment, img_name in values:
            # Process img_name to remove the "../../" that is currently preceding each file name
            img_name = os.path.basename(img_name)
            # Add all the fields in the correct order and format to the string that will be written to the .txt file
            output_content += f"\n\nBeginning processing of {filename} annotation number {curr_annotation_num}\n"
            output_content += f"\"file_name\": \"{img_name}\",\n"
            output_content += f"\"category_id\": 0,\n"
            output_content += f"\"bbox\": {bbox},\n"
            output_content += f"\"bbox_mode\": 1,\n"
            # Call the helper function to get the are and segmentation data
            area, s = polygonarea_and_segmentationformat(segment)
            output_content += f"\"segmentation\": [{s}],\n"
            output_content += f"\"area\": {area}\n"
            curr_annotation_num += 1
        write_to_file(output_filepath, output_content)
        print("Output saved to:", output_filepath)





