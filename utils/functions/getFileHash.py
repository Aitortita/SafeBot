import aiohttp
import hashlib

# Function to get the file hash from a file via its URL
async def get_file_hash(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                # Start a new hash256
                hash_sha256 = hashlib.sha256()
                # Reads the file in chunks to avoid downloading the entire file into memory
                async for chunk in response.content.iter_any():
                    hash_sha256.update(chunk)
                return hash_sha256.hexdigest()
            else:
                raise Exception("Failed to fetch the file")