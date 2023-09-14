import base64

def url_id_generator(url: str):
    return base64.urlsafe_b64encode(url.encode()).decode().strip("=")