#!/bin/bash

ENDPOINT_URL=${1:-'http://localhost:4566'}
AWS="aws --endpoint-url=${ENDPOINT_URL}"
BUCKET_NAME="model-localstack"
BUCKET_CONFIG="LocationConstraint=ap-northeast-3"

$AWS s3api create-bucket --bucket $BUCKET_NAME --create-bucket-configuration $BUCKET_CONFIG

$AWS s3 cp ./model-files/ s3://$BUCKET_NAME --recursive