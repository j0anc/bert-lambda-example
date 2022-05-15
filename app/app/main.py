
import json
from os import getenv
from inference import load_tokenizer_model, inference, postprocessing, id2label


def handler(event, context):

    # get text for inference from the event object
    event_body_dict = json.loads(event["body"])
    text = event_body_dict["text"]

    # get s3 bucket name and endpoint from environment variable
    s3_endpoint_url = getenv("LOCALSTACK_S3_ENDPOINT", None)
    s3_bucket_name = getenv("S3_BUCKET_NAME", None)

    model, tokenizer = load_tokenizer_model(s3_endpoint_url, s3_bucket_name)
    pred_raw = inference(text, model, tokenizer)
    final_result = postprocessing(pred_raw, id2label)

    lambda_result = {"statusCode": 200,
                     "body": json.dumps(final_result)}

    return lambda_result
