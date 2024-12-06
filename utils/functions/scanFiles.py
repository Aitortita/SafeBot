import discord
import asyncio
from . import scan_file, get_file_hash

async def scan_files(attachments: list[discord.Attachment]) -> list[dict]:
    """
  This function scans a list of files and returns the results.

  Args:
    attachments: A list of files to scan.

  Returns:
    a list of dict containing the results of the scan.
    """
    
    # Calculate file hashes
    fileHashes = await asyncio.gather(*[
        get_file_hash(attachment.url) for attachment in attachments
    ])
    
    # Create asynchronous scan tasks for each attachment and its hash.
    scans = [scan_file(attachment, fileHash) for attachment, fileHash in zip(attachments, fileHashes)]

    # Run all scans concurrently
    results = await asyncio.gather(*scans)

    return results