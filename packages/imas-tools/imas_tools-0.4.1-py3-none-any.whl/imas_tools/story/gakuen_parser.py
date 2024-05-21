import json


def parse_identifier(message, i):
    j = i
    while message[i].isalnum() or message[i] == "_":
        i = i + 1
    return i, message[j:i]


def parse_string(message, i):
    j = i
    while message[i] != " " and message[i] != "]":
        i = i + 1
    return i, message[j:i]


def parse_json(message, i):
    j = i
    if message[i : i + 2] != r"\{":
        raise ValueError()
    n = 1
    i = i + 2
    while n > 0:
        if i + 2 <= len(message):
            if message[i : i + 2] == r"\{":
                n = n + 1
                i = i + 2
                continue
            elif message[i : i + 2] == r"\}":
                n = n - 1
                i = i + 2
                continue
        i = i + 1
    obj = json.loads(message[j:i].replace(r"\{", "{").replace(r"\}", "}"))
    if "__tag__" in obj:
        raise ValueError()
    return i, obj


def parse_object(message, i):
    if message[i] != "[":
        raise ValueError()
    i = i + 1
    i, tag = parse_identifier(message, i)
    obj = {"__tag__": tag}
    while message[i] != "]":
        if message[i] != " ":
            raise ValueError()
        i = i + 1
        i, key = parse_identifier(message, i)
        if key == "__tag__":
            raise ValueError()
        if message[i] != "=":
            raise ValueError()
        i = i + 1
        if i + 2 <= len(message) and message[i : i + 2] == r"\{":
            i, value = parse_json(message, i)
        elif message[i] == "[":
            i, value = parse_object(message, i)
        else:
            i, value = parse_string(message, i)
        if key not in obj:
            obj[key] = value
        elif type(obj[key]) is list:
            obj[key].append(value)
        else:
            obj[key] = [obj[key], value]
    if message[i] != "]":
        raise ValueError()
    i = i + 1
    return i, obj


def parse_message(message: str):
    i, o = parse_object(message, 0)
    if i != len(message):
        raise ValueError()
    return o


def parse_messages(messages: str) -> list:
    return [
        parse_message(message) for message in messages.split("\n") if message.strip()
    ]


def encode_json(obj):
    return (
        json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
        .replace("{", r"\{")
        .replace("}", r"\}")
    )


def encode_message_kv(k, v):
    if k == "__tag__":
        if type(v) is not str:
            raise ValueError()
        return v
    if type(v) is list:
        return " ".join([encode_message_kv(k, w) for w in v])
    if type(v) is str:
        return f"{k}={v}"
    if type(v) is not dict:
        raise ValueError
    if "__tag__" in v:
        return f"{k}={encode_message(v)}"
    return f"{k}={encode_json(v)}"


def encode_message(obj):
    return (
        "["
        + " ".join(
            [obj["__tag__"]]
            + [encode_message_kv(k, v) for k, v in obj.items() if k != "__tag__"]
        )
        + "]"
    )
