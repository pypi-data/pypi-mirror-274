def camel_to_snake(camelCase: str):
    return "".join(["_" + c.lower() if c.isupper() else c for c in camelCase]).lstrip(
        "_"
    )
