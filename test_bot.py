from bot import answer, classify


def test_classify():
    assert classify("How much is the Pro plan?") == "pricing"
    assert classify("Where is my order?") == "account"
    assert classify("What are your support hours?") == "faq"


def test_answer_calls_model():
    assert answer("What are your support hours?").startswith("[model answer")
