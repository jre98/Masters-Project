import json
import cv2
from detectron2.utils.visualizer import Visualizer

# Get file path to json label file
labels_path = "/Users/jacob/Desktop/CPSC 597/detectronDataset/aaaddd.json"

# Read the dataset dictionary from the JSON file
with open(labels_path, "r") as f:
    dataset_dict = json.load(f)

# Prompt the user to enter the image file name
image_file_name = input("Enter the image file name: ")

# Find the image ID for the specified image file name
image_id = next((image["id"] for image in dataset_dict["images"] if image["file_name"] == image_file_name), None)

# Check if the image ID is found
if image_id is not None:
    # Find annotations for the specified image
    annotations = [ann for ann in dataset_dict["annotations"] if ann["image_id"] == image_id]

    # Read the specified image
    img = cv2.imread("/Users/jacob/Desktop/CPSC 597/detectronDataset/" + image_file_name)

    # Visualize the specified image with its associated labels
    visualizer = Visualizer(img[:, :, ::-1], scale=0.5)
    out = visualizer.draw_dataset_dict({"annotations": annotations})
    # Give window a title that includes the current image file name
    window_title = image_file_name + " Plus Label(s)"
    # Show window and keep displayed until user presses a key
    cv2.imshow(window_title, out.get_image()[:, :, ::-1])
    cv2.waitKey(0)
# If the image ID was not found, display an appropriate error message
else:
    print("Image file name not found in annotations.")
