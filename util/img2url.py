import base64

def image_bytes_to_url(image_bytes: bytes, mime_type: str = "image/png") -> str:
    base64_str = base64.b64encode(image_bytes).decode("utf-8")
    with open("test.txt", 'w', encoding='utf-8') as file:
        file.write(f"data:{mime_type};base64,{base64_str}")
    return f"data:{mime_type};base64,{base64_str}"