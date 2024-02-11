import cv2
import glob
import numpy as np
import os
import sys
import microplastic_analysis

# define the minimum confidence (to filter weak detections)
confidence_thresh = 0.5
# Non-Maximum Suppression (NMS) threshold
NMS_thresh = 0.3
# color to draw bounds
green = (0, 255, 0)
# label of detected object
label = "Microplastics"

yolo_config = "yolov4.cfg"
yolo_weights = "yolov4.weights"

# returns image opened using OpenCV
def open_image(image_path):
    f = open(image_path, "rb")
    chunk = f.read()
    chunk_arr = np.frombuffer(chunk, dtype=np.uint8)
    image = cv2.imdecode(chunk_arr, cv2.IMREAD_COLOR)
    return image

# returns boxes of found microplastics, indices of confident values and confidences
def detect_microplastics(image):
    # get the image dimensions
    h = image.shape[0]
    w = image.shape[1]

    # load the YOLOv4 pre-trained network
    net = cv2.dnn.readNetFromDarknet(yolo_config, yolo_weights)

    # get the name of all the layers in the network
    layer_names = net.getLayerNames()

    # get the names of the output layers
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

    # create a blob from the image
    blob = cv2.dnn.blobFromImage(image, 1 / 255, (416, 416), swapRB=True, crop=False)

    # pass the blob through the network and get the output predictions
    net.setInput(blob)
    outputs = net.forward(output_layers)

    # create empty lists for storing the bounding boxes and confidences
    boxes = []
    confidences = []

    # loop over the output predictions
    for output in outputs:
        # loop over the detections
        for detection in output:
            # get the confidence of the detected object
            confidence = detection[5]

            # we keep the bounding boxes if the confidence (i.e. class probability)
            # is greater than the minimum confidence
            if confidence > confidence_thresh:
                # perform element-wise multiplication to get
                # the coordinates of the bounding box
                box = [int(a * b) for a, b in zip(detection[0:4], [w, h, w, h])]
                center_x, center_y, width, height = box

                # get the top-left corner of the bounding box
                x = int(center_x - (width / 2))
                y = int(center_y - (height / 2))

                # append the bounding box and the confidence to their respective lists
                confidences.append(float(confidence))
                boxes.append([x, y, width, height])

    # apply non-maximum suppression to remove weak bounding boxes that overlap with others.
    indices = cv2.dnn.NMSBoxes(boxes, confidences, confidence_thresh, NMS_thresh)

    return boxes, indices, confidences

# draws bounds on image
def draw_bounds(image, boxes, indices, confidences):
    # loop over the indices only if the `indices` list is not empty
    if len(indices) > 0:
        # loop over the indices
        for i in indices.flatten():
            (x, y, w, h) = boxes[i][0], boxes[i][1], boxes[i][2], boxes[i][3]
            cv2.rectangle(image, (x, y), (x + w, y + h), green, 2)
            particle_image = image[y:y+h, x:x+w]
            particle_color = microplastic_analysis.anylize_color(image)
            text = f"{label}: {confidences[i] * 100:.2f}% {particle_color} color"
            cv2.putText(image, text, (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, green, 2)

# open a window with image
def show_image(image):
    cv2.imshow("Image", image)
    cv2.waitKey(0)

# save image
def save_image(image, image_path, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    filename = os.path.basename(image_path)
    cv2.imwrite(os.path.join(output_path, "$.png"), image)
    try:
        os.remove(os.path.join(output_path, "result_" + filename))
    except OSError:
        pass
    os.rename(os.path.join(output_path, "$.png"), os.path.join(output_path, "result_" + filename))


if __name__ == '__main__':
    args = sys.argv
    image_path = "PhotosInfo/" + args[1] + "/" + args[1]
    image = open_image(image_path)
    boxes, indices, confidences = detect_microplastics(image)
    draw_bounds(image, boxes, indices, confidences)
    save_image(image, image_path, "PhotosInfo/" + args[1] + "/")
        