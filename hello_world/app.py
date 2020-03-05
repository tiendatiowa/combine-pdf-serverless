import json
import io
import PyPDF2
from urllib.request import urlopen
import boto3


class InvalidInput(Exception):
    def __init__(self, message):
        self.message = message


class InvalidPdfContent(Exception):
    def __init__(self, message):
        self.message = message


class UnableToUploadToS3(Exception):
    def __init__(self, message):
        self.message = message


def uploadToS3(bucket, key, body):
    try:
        s3 = boto3.client('s3')
        response = s3.put_object(
            Bucket=bucket,
            Key=key,
            Body=body
        )
        return response
    except:
        raise UnableToUploadToS3("Unable to upload content to S3 bucket '{}' and key '{}'".format(bucket, key))


def mergeContentOfUrl(url, writer):
    try:
        remoteFile = urlopen(url).read()
        memoryFile = io.BytesIO(remoteFile)
        pdfFile = PyPDF2.PdfFileReader(memoryFile)

        for pageNum in range(pdfFile.getNumPages()):
            currentPage = pdfFile.getPage(pageNum)
            writer.addPage(currentPage)
    except:
        raise InvalidPdfContent("Could not extract content from URL '{}'".format(url))


def extractParamFromEvent(event, paramName):
    try:
        return event[paramName]
    except:
        raise InvalidInput("Event doesn't have param with name '{}'".format(paramName))


def lambda_handler(event, context):
    try:
        urls = extractParamFromEvent(event, "input")  # list of URLs for input PDFS, e.g. S3 path to these PDFs
        if len(urls) == 0:
            raise InvalidInput("There's no URL in the 'input' param")

        bucket = extractParamFromEvent(event, "bucket")  # the bucket to write the output PDF
        if len(bucket) == 0:
            raise InvalidInput("The 'bucket' param is empty")

        key = extractParamFromEvent(event, "output")  # the name of the output PDF
        if len(key) == 0:
            raise InvalidInput("The 'output' param is empty")

        writer = PyPDF2.PdfFileWriter()

        for url in urls:
            mergeContentOfUrl(url, writer)

        outputStream = io.BytesIO()
        writer.write(outputStream)
        outputContent = outputStream.getvalue()

        res = uploadToS3(bucket, key, outputContent)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Combine {} pdfs successfully".format(len(urls)),
                "response": res
            })
        }
    except InvalidInput as ex:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "Event is invalid",
                "event": event,
                "exception": ex.message
            })
        }
    except InvalidPdfContent as ex:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "Content of URL is invalid",
                "event": event,
                "exception": ex.message
            })
        }
    except UnableToUploadToS3 as ex:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "Unable to upload result to S3",
                "event": event,
                "exception": ex.message
            })
        }
    except Exception as ex:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "Unable to process event",
                "event": event,
                "exception": str(ex)
            })
        }
