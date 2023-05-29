# S3 File Uploader

This project contains a class with four methods for working with Amazon S3:

## get_credentials

Returns the credentials for the service, which are retrieved from the `config.py` file.

## get_client

Returns the client for the Amazon S3 service. This method creates a client for accessing S3 and is used by the `upload_file` and `get_file_url` methods.

## upload_file

Uploads a file to the specified S3 bucket. It takes a PDF file as input (if you need to handle different file types, please let me know), defines the `object_name` (the key under which the file will be stored in the bucket), and uses the `get_file_url` method to generate a presigned URL for the uploaded file. If you don't need to return a URL, I can modify the function accordingly.

## get_file_url

Returns the presigned URL of the file uploaded to the specified S3 bucket. The URL is generated based on the `object_name` (the key of the file in the bucket). Please ensure that the appropriate permissions are set on the bucket to control access to the uploaded files. The link provided in this method includes `ExtraArgs={ 'ContentDisposition': 'inline'}` to ensure that the file is opened in the browser instead of being downloaded.

To test the functionality, an `app.py` file is included that utilizes FastAPI. You can access it at `http://127.0.0.1:8000/docs`.

Before running the application, make sure to create a `.env` file that includes the following variables:

- `aws_access_key_id`: The AWS access key ID.
- `aws_secret_access_key`: The AWS secret access key.
- `bucket_name`: The name of the S3 bucket.
- `expiration`: The expiration time for the presigned URLs.

Please set these variables in the `.env` file before running the application.

