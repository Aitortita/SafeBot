import base64

def url_id_generator(url: str) -> str:
    """
    Transform a url into its base64 encoded version 

    Args:
        url: The URL to transform.

    Returns:
        The base64 encoded URL.
    """
    return base64.urlsafe_b64encode(url.encode()).decode().strip("=")