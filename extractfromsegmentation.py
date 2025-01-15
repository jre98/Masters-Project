import json

def extract_segmentation_and_bbox(json_file_path):
    with open(json_file_path, 'r') as f:
        data = json.load(f)

    extracted_values = []

    for item in data:
        for annotation in item['annotations']:
            bbox = annotation['bbox']
            segmentation = annotation['segmentation'][0]

            extracted_values.append((bbox, segmentation))

    return extracted_values

# Example usage:
json_file_path = '/Users/jacob/Desktop/CPSC 597/detectron items/jsonConversion/Post Conversion/TMPEastmanParkGB.json'
values = extract_segmentation_and_bbox(json_file_path)
for v in values:
    bbox, segmentation = v
    print("Bounding Box:", bbox)
    print("Segmentation:", segmentation)
    print()
