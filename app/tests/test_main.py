from os import path, getenv
from dotenv import load_dotenv
import transformers
import torch
import json

from app.inference import (
    load_tokenizer_model,
    model_inference,
    postprocessing,
    id2label,
)
from app.main import handler
from tests.fixtures import *

# ========== helper functions ==========

# setup environment variables for localstack
def getS3EnvInfo():
    try:
        dotenv_path = path.join(path.dirname(__file__), "../.env")
        load_dotenv(dotenv_path)
    except:
        pass
    s3_bucket_name = getenv("S3_BUCKET_NAME", None)
    s3_endpoint_url = getenv("LOCALSTACK_ENDPOINT", None)
    return s3_bucket_name, s3_endpoint_url


# generate lambda event object
def generate_test_event(text):
    event_body_str = json.dumps({"text": text})
    event_data = {"body": event_body_str}
    return event_data


# ========== unittest ==========


def test_load_model_tokenizer():
    s3_bucket_name, s3_endpoint_url = getS3EnvInfo()
    print(s3_bucket_name, s3_endpoint_url)
    model, tokenizer = load_tokenizer_model(s3_endpoint_url, s3_bucket_name)
    assert (
        type(model)
        == transformers.models.bert.modeling_bert.BertForSequenceClassification
    )
    assert (
        type(tokenizer)
        == transformers.models.bert.tokenization_bert_fast.BertTokenizerFast
    )


def test_inference(test_text):
    s3_bucket_name, s3_endpoint_url = getS3EnvInfo()
    model, tokenizer = load_tokenizer_model(s3_endpoint_url, s3_bucket_name)

    pred_logits = model_inference(test_text, model, tokenizer)
    assert type(pred_logits) == torch.Tensor


def test_postprocessing(test_logit):
    pred_labels = postprocessing(test_logit, id2label)
    assert pred_labels == ["anger", "fear"]


# ========== integration test ==========


def test_handler_case1(expected_output_case1, test_text):
    s3_bucket_name, s3_endpoint_url = getS3EnvInfo()
    event = generate_test_event(test_text)
    result = handler(event, context={})
    assert result == expected_output_case1


def test_headler_case2(expected_output_case2):
    event = {}
    result = handler(event, context={})
    assert result == expected_output_case2
