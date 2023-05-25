import logging

from fastapi import FastAPI,  UploadFile, File
from fastapi.responses import JSONResponse

from upload_pdf_to_s3 import AWSLoadS3


app = FastAPI()


@app.post("/upload")
def upload(file: UploadFile = File(...)):
    try:
        url = AWSLoadS3.upload_file(file)
        if url:
            return JSONResponse(status_code=200, content={"message": f"File uploaded successfully. \n The url of the file: {url}"})
        else:
            return JSONResponse(status_code=500, content={"message": "An error occurred during the file upload."})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})


@app.get('/url')
def get_url(object_name):
    try:
        url =  AWSLoadS3.get_file_url(object_name)
    except Exception as e:
        logging.error(e)
        return JSONResponse(status_code=500, content={"message": str(e)})
        
    return JSONResponse(status_code=200, content={"message": f"The url of the doc in AWS S3: {url}"})

