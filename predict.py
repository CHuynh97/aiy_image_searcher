import logging
from darkflow.net.build import TFNet
import cv2
import sys


logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)

model = None


def init_model(options):
    """
    Initialize a darknet model
    :param options: dict that contain config file, wieght file and thresholds to use for model
    """
    global model
    model = TFNet(options)
    logger.info("Model initialized")
    logger.info("Using config file: {}".format(options["model"]))
    logger.info("Using weight file: {}".format(options["load"]))
    logger.info("Using threshold: {}".format(options["threshold"]))


def detect_centre_object(img):
    """
    Use darknet model for object detection and grab the most centred object in the image
    :param img: numpy.ndarray that represents the image to predict
    """
    global model
    res = model.return_predict(img)
    img_centre = (
        img.shape[0]/2,
        img.shape[1]/2
    )
    obj_center_list = []
    for obj in res:
        tl = obj["topleft"]
        br = obj["topleft"]
        center = (
            (tl["x"]+br["x"])/2 - img_centre[0],
            (tl["y"]+br["y"])/2 - img_centre[1]
        )
        obj_center_list.append(center[0] + center[1])
    center_idx = obj_center_list.index(min(obj_center_list))
    center_obj = res[center_idx]
    print(center_obj["label"])


if __name__ == "__main__":
    options = {
        "model": "cfg/yolo.cfg",
        "load": "weights/yolo.weights",
        "threshold": 0.5
    }
    init_model(options)
    img_file = sys.argv[1]
    logger.info("Predicting {}".format(img_file))
    img = cv2.imread(img_file)
    detect_centre_object(img)
