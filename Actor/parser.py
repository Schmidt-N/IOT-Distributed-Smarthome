def decode(msg):
    msg_str = msg.decode("utf-8")
    
    lines = msg_str.strip().split("\n")
    
    parsed_data = {
        "Header": {},
        "Payloads": []
    }

    current_section = None
    current_payload = None

    for line in lines:
        line = line.strip()
        
        if not line or line.startswith(";"):
            continue
        
        if line.startswith("[") and line.endswith("]"):
            section_name = line[1:-1]
            if section_name == "Header":
                current_section = "Header"
            elif section_name == "Payload":
                current_section = "Payload"
                current_payload = {}
                parsed_data["Payloads"].append(current_payload)
            continue
        
        if "=" in line:
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()
            
            if current_section == "Header":
                parsed_data["Header"][key] = value
            elif current_section == "Payload" and current_payload is not None:
                current_payload[key] = value
    
    return parsed_data