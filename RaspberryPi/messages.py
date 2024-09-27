def build_message(header, payloads):
    """
    Baut eine Nachricht im gewünschten Format zusammen.
    
    :param header: Ein Dictionary mit den Header-Informationen (Sender, Receiver, MessageID)
    :param payloads: Eine Liste von Dictionaries, die die Payload-Daten enthalten (Type, Value)
    :return: Die formatierte Nachricht als String
    """
    message = "[Header]\n"
    for key, value in header.items():
        message += f"{key}={value}\n"
    
    for payload in payloads:
        message += "\n[Payload]\n"
        for key, value in payload.items():
            message += f"{key}={value}\n"
    
    return message.strip()