from pypeg2 import *

class String(str):
    grammar = re.compile(r"[a-zA-Z0-9-]+")

class Number(int):
    grammar = re.compile(r"-?\d+(.\d+)?")

class Key(Namespace):
    grammar = attr("key", String)

class ValueString(Namespace):
    grammar = attr("value", String)

class ValueNumber(Namespace):
    grammar = attr("number", Number)

class Header(Namespace):
    grammar = "[Header]", endl, \
              String,"=", attr("sender", String), endl

class Payload(Namespace):
    grammar = "[Payload]", endl, \
              String,"=", attr("value", Number), endl, \
              String,"=", attr("type", String), endl

class Message(Namespace):
    grammar = attr("header",Header), attr("payload", Payload)
