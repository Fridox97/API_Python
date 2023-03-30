# import required libraries
import cv2
import numpy as np
from fastapi import FastAPI, UploadFile, File

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hola mundo"}

@app.post("/detect_person")
async def detect(image: UploadFile = File(...)):
    # Reading the Image
    contents = await image.read()
    nparr = np.fromstring(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # initialize the HOG descriptor
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    # detect humans in input image
    (humans, _) = hog.detectMultiScale(img, winStride=(10, 10), padding=(32, 32), scale=1.1)

    # getting no. of human detected
    return {"Humanos": len(humans)}


