import base64

def url_id_generator(urls: list) -> list:
    encoded_urls: list = []
    for url in urls:
        encoded_urls.append(base64.urlsafe_b64encode(url.encode()).decode().strip("="))
    return encoded_urls