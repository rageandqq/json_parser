class Tokenizer:

    json_string = None
    peeked_token = None
    position = None

    def __init__(self, json_string):
        self.json_string = json_string
        self.position = 0

    def next():
        raise NotImplementedError

    def peek():
        if not peeked_token:
            peeked_token = self.next()
        return peeked_token
