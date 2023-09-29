from . import scan_url
import asyncio

# automatic scan function using requests on virus total api
async def scan_urls(urls: list[str]) -> list[dict]:
    """
  This function scans a list of URLs and returns the results.

  Args:
    urls: A list of URLs to scan.

  Returns:
    A list of dict containing the results of the scan.
    """
    # Create a list of asynchronous scans to scan each URL.
    scans = [scan_url(url) for url in urls]

    # Start all of the scans at the same time and wait for them to complete.
    results = await asyncio.gather(*scans)

    return results