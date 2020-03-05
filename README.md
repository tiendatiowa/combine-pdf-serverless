# combine-pdf-serverless

A serverless function to combine multiple PDFs into one

## Environment

- Python3.7
- SAM CLI, version 0.43.0

If you have not done so, following the steps to install 
the [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
on your local machine. Also recommend installing Docker to test code locally.

## Execute the code locally

In your console, execute:

`sam build`

to build the code, then execute:

`sam local invoke -e input.json`

to test the code locally. Note that you'll need to modify the input.json file to
include the correct links to the PDFs you want to combine, and the S3 bucket and
output file name. If your input.json is correct, you'll see a result like this
in  the console:

`$ sam local invoke -e input.json`

`Invoking app.lambda_handler (python3.7)`
``
`Fetching lambci/lambda:python3.7 Docker container image......`

`Mounting /Users/datnguyen/works/tiendatiowa/sam/combine-pdf/.aws-sam/build/HelloWorldFunction as /var/task:ro,delegated inside runtime container`

`START RequestId: fea61f91-0df7-1b00-24b1-7af880e609b1 Version: $LATEST`

`END RequestId: fea61f91-0df7-1b00-24b1-7af880e609b1`

`REPORT RequestId: fea61f91-0df7-1b00-24b1-7af880e609b1	Init Duration: 407.83 ms	Duration: 646.80 ms	Billed Duration: 700 ms	Memory Size: 128 MB	Max Memory Used: 41 MB`	

`{"statusCode":200,"body":"{\"message\": \"Combine 2 pdfs successfully\", \"response\": {\"ResponseMetadata\": {\"RequestId\": \"EFE3CAEC05E2EFFE\", \"HostId\": \"hDj2QuWwAl9Frfq/Y1ZT5+vggMuV0e1Uxv5E8q26yRAxaxAU9CfoiW0B/xyW9o/TFKla34kMFZ4=\", \"HTTPStatusCode\": 200, \"HTTPHeaders\": {\"x-amz-id-2\": \"hDj2QuWwAl9Frfq/Y1ZT5+vggMuV0e1Uxv5E8q26yRAxaxAU9CfoiW0B/xyW9o/TFKla34kMFZ4=\", \"x-amz-request-id\": \"EFE3CAEC05E2EFFE\", \"date\": \"Thu, 05 Mar 2020 19:59:08 GMT\", \"x-amz-version-id\": \"d5DRRcbdtIXATMIdYoem2gIiRjyIST.3\", \"etag\": \"\\\"1130363fcaccbdf128bd2f574d7eb74a\\\"\", \"content-length\": \"0\", \"server\": \"AmazonS3\"}, \"RetryAttempts\": 1}, \"ETag\": \"\\\"1130363fcaccbdf128bd2f574d7eb74a\\\"\", \"VersionId\": \"d5DRRcbdtIXATMIdYoem2gIiRjyIST.3\"}}"}`

If you open the S3 bucket, you should see the output file there.

## Deploy the code to AWS

In your console, execute:

`sam deploy --guided`

and follow the guided instruction to deploy the serverless function to AWS.