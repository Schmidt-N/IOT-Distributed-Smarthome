from pypeg2 import *

Symbol.regex = re.compile(r"[\w\s]+")

class Key(str):
    grammar = name(), "=", restline, endl

class Header(Namespace):
    grammar = "[", "Header", "]", endl, maybe_some(Key)

class Payload(Namespace):
    grammar = "[", "Payload", "]", endl, maybe_some(Key)

class Message(Namespace):
    grammar = maybe_some(Header), maybe_some(Payload)
