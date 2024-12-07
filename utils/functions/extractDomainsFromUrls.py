from urllib.parse import urlparse

# function to extract urls from user's messages
def extract_domains_from_urls(urls: list[str]) -> list[str]:
    domains = []
    for url in urls:
        parsed_url = urlparse(url)
        # Get the netloc (domain) from the parsed URL
        domain = parsed_url.netloc
        # Split the domain by dots and take the last two parts to get the main domain
        domain_parts = domain.split('.')
        main_domain = '.'.join(domain_parts[-2:])
        domains.append(main_domain)
    return domains