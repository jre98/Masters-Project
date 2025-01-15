from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2 import model_zoo
import cv2
from detectron2.data import MetadataCatalog
from detectron2.utils.visualizer import Visualizer, ColorMode

# Get input from user on which image should be predicted on. Also include a message to the 
# user to ensure the files are in the proper directories
image_to_predict = input(
    "Please input an image file to predict on.\n Please ensure that the file name is in the \"Test\" folder"  
    " of the detectronDataset, and that the dataset folder is in the same directory as this program file: ")

# Construct full image filepath:
img_filepath = '/Users/jacob/Desktop/CPSC 597/detectronDataset/Test/' + image_to_predict

# Get cfg to work with model
cfg = get_cfg()
# Predictions only need to use the cpu
cfg.MODEL.DEVICE = "cpu"
# This line is supposed to filter out predictions with a certainty score lower than 40%, 
# but it would not work and kept showing no predictions at all
# cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.4 

# Get the model configuration from the model zoo
cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
# Get the trained model weights
cfg.MODEL.WEIGHTS = "/Users/jacob/Desktop/Master's Project Submission/model_final.pth"
# Create a predictor instance that will actually make the prediction 
predictor = DefaultPredictor(cfg)
# Read the image file that will be predicted on
im = cv2.imread(img_filepath)
# Use the predictor instance to make a prediction on the image, store the predictions in "outputs"
outputs = predictor(im)

# Create a visualizer instane to visualize the predictions
v = Visualizer(im[:, :, ::-1], scale=0.5)
# Draw the predictions on the image, store the image + predictions to a new variable, "out"
out = v.draw_instance_predictions(outputs["instances"].to("cpu"))
# Convert the image + predictions to a regular color image that cv2 can recognize
img = cv2.cvtColor(out.get_image()[:, :, ::-1], cv2.COLOR_RGBA2RGB)
win_title = "Predictions on Image File " + image_to_predict
# Use cv2.imshow to display the image and its prediction
cv2.imshow(win_title, out.get_image()[:, :, ::-1])
cv2.waitKey(0)

