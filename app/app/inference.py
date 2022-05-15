import torch
import numpy as np
import boto3
from transformers import AutoModelForSequenceClassification, AutoTokenizer

labels = ['anger', 'anticipation', 'disgust', 'fear', 'joy',
          'love', 'optimism', 'pessimism', 'sadness', 'surprise', 'trust']
id2label = {idx: label for idx, label in enumerate(labels)}


def load_tokenizer_model(s3_endpoint_url, s3_bucket_name):

    tmp_path = "/tmp/"

    s3 = boto3.resource("s3", endpoint_url=s3_endpoint_url)

    S3_BUCKET_NAME = s3_bucket_name
    files = [
        "pytorch_model.bin",
        "config.json",
        "sentencepiece.bpe.model",
        "special_tokens_map.json",
        "tokenizer_config.json",
        "tokenizer.json",
    ]

    for file in files:
        s3.Bucket(S3_BUCKET_NAME).download_file(file, tmp_path + file)

    model = AutoModelForSequenceClassification.from_pretrained(tmp_path)
    tokenizer = AutoTokenizer.from_pretrained(tmp_path)
    return model, tokenizer


def inference(text, model, tokenizer):
    encoded_text = tokenizer(text, return_tensors="pt",
                             padding="max_length", truncation=True, max_length=128)
    encoded_text_dict = {k: v for k, v in encoded_text.items()}
    model.eval()
    outputs = model(**encoded_text_dict)
    logits = outputs.logits
    return logits


def postprocessing(logits, id2label_dict):
    sigmoid = torch.nn.Sigmoid()
    prob = sigmoid(logits.squeeze().cpu())
    pred = np.zeros(prob.shape)
    pred[np.where(prob >= 0.5)] = 1
    pred_labels = [id2label_dict[idx]
                   for idx, label in enumerate(pred) if label == 1.0]
    return pred_labels
