from urllib.parse import urlparse

# Function to extract domain from URL
def extract_domain(url: str) -> str:
    parsed_url = urlparse(url)
    # Get the netloc (domain) from the parsed URL
    domain = parsed_url.netloc
    # Split the domain by dots and take the last two parts to get the main domain
    domain_parts = domain.split('.')
    main_domain = '.'.join(domain_parts[-2:])
    return main_domain