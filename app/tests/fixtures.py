import pytest
import torch
import json


@pytest.fixture
def test_text():
    return "This is the best strawberry cake I have ever had."


@pytest.fixture
def test_logit():
    return torch.tensor(
        [[5, -2, -4, 3, -5, -1, -1, -4, -3, -2, -1]], dtype=torch.float32
    )


@pytest.fixture
def expected_output_case1():
    final_result = ["joy", "love", "optimism"]
    result = {"statusCode": 200, "body": json.dumps(final_result)}
    return result


@pytest.fixture
def expected_output_case2():
    final_result = {"message": "unexpected error"}
    result = {"statusCode": 500, "body": json.dumps(final_result)}
    return result
