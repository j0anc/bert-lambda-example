import json
import sys
from os import getenv
from app.inference import (
    load_tokenizer_model,
    model_inference,
    postprocessing,
    id2label,
)


def handler(event, context):

    print("event", event)

    try:

        # get text for inference from the event object
        event_body_dict = json.loads(event["body"])
        text = event_body_dict["text"]
        print("text", text)

        # get s3 bucket name and endpoint from environment variable
        s3_endpoint_url = getenv("LOCALSTACK_ENDPOINT", None)
        s3_bucket_name = getenv("S3_BUCKET_NAME", None)

        model, tokenizer = load_tokenizer_model(s3_endpoint_url, s3_bucket_name)
        pred_raw = model_inference(text, model, tokenizer)
        final_result = postprocessing(pred_raw, id2label)

        status_code = 200

    except BaseException as e:

        final_result = {"message": "unexpected error"}
        print("unexpected error", e, file=sys.stderr)
        status_code = 500

    lambda_result = {"statusCode": status_code, "body": json.dumps(final_result)}

    return lambda_result
