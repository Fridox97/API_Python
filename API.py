# import required libraries
import cv2
import numpy as np
from fastapi import FastAPI, UploadFile, File

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hola mundo"}

@app.post("/detectar")
async def detect(image: UploadFile = File(...)):
    # Reading the Image
    contents = await image.read()
    nparr = np.fromstring(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    personas = 0
    perro = 0
    gato = 0

    model = cv2.dnn.readNetFromCaffe('MobileNetSSD_deploy.prototxt.txt',
                                     'MobileNetSSD_deploy.caffemodel')

    # Resize image to a fixed width of 300 pixels (the input size of the model)
    image_resized = cv2.resize(img, (300, 300))

    # Preprocess the image by subtracting the mean RGB values and scaling by a factor of 0.007843
    blob = cv2.dnn.blobFromImage(image_resized, 0.007843, (300, 300), (127.5, 127.5, 127.5), False)

    # Set the input to the model
    model.setInput(blob)

    # Run the forward pass through the model to detect objects in the image
    detections = model.forward()

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        class_id = int(detections[0, 0, i, 1])
        # If the confidence score is above a certain threshold (e.g., 0.5), treat it as a detection
        if confidence > 0.8 and class_id == 15:
            personas += 1

        if confidence > 0.6 and class_id == 12:
            perro += 1

        if confidence > 0.5 and class_id == 8:
            gato += 1

    return {"humanos": personas,
            "gatos": gato,
            "perros": perro}
