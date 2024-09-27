from pypeg2 import *

def number():
    return re.compile(r"-?\d+(.\d+)?")

def custom_name():
    return re.compile(r"[a-zA-Z0-9-]+")

class Header(Namespace):
    grammar = "[Header]", endl, \
              custom_name(),"=", attr("sender", custom_name()), endl

class Payload(Namespace):
    grammar = "[Payload]", endl, \
              custom_name(),"=", attr("value", number()), endl, \
              custom_name(),"=", attr("type", custom_name()), endl
class Message(Namespace):
    grammar = attr("header",Header), attr("payload", Payload)
