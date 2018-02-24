from picamera import PiCamera
from picamera.array import PiRGBArray
import time
from darkflow.net.build import TFNet


def get_bgr_snapshot(camera):
    raw_capture = PiRGBArray(camera)
    camera.capture(raw_capture, format="bgr")
    return raw_capture.array


def predict(model, image):
    return model.return_predict(image)


# Get command line args
args = sys.args[1:]

if len(args) != 3:
    print("Usage: python image_predict.py <model> <load> <threshold>")
    exit(1)

options = {
    "model": args[0],
    "load": args[1],
    "threshold": float(args[2])
}

# Initialize model and Camera
TF = TFNet(options)
camera = PiCamera()

time.sleep(0.1)

# Main loop
while True:
    # TODO Implement if statement to trigger image capture on audio input
    # if <Audio Input> == "what's that" or "what is that"
    x = input()
    if x == "s":
        img = get_bgr_snapshot(camera=camera)
        img_centre = (
            img.shape[0]/2,
            img.shape[1]/2
        )
        res = predict(model=TF, image=img)
        
        # Choose the most centered object
        center_obj = None
        obj_center_list = []
        for obj in res:
            tl = obj["topleft"]
            br = obj["topleft"]
            center = (
                (tl["x"]+br["x"])/2 - img_centre[0],
                (tl["y"]+br["y"])/2 - img_centre[1]
            )
            obj_center_list.apend(center[0] + center[1])
        center_idx = min(obj_center_list)
        center_obj = res[center_idx]["label"]
        # Send object to kafka stream
        # kafka_produce
        print(center_obj)


    
    
