import discord
import aiohttp
import asyncio
import config.settings as settings
from .handleVtAnalysis import handle_vt_analysis
from logging import getLogger
bot = getLogger("bot")
scans = getLogger("scans")

headers = {
    "accept": "application/json",
    "X-Apikey": settings.VIRUSTOTAL_API_KEY
}

async def scan_file(file: discord.Attachment, fileHash: str) -> dict:
    """
    Scan a single File and return the results.

    Args:
        file: The File to scan.

    Returns:
        A Dict containing the results of the scan.
    """
    try:
        async with aiohttp.ClientSession() as session:
            # Make an asynchronous request to VirusTotal to check if there is an analysis of the file.
            response = await session.get(f"https://www.virustotal.com/api/v3/files/{fileHash}", headers=headers)

            if (response.status == 200):
                scans.info(f"Scanning file:{file.filename} with hash: {fileHash}")
                # If the request was successful it means that an already made analysis exists, so we need to ask VirusTotal to reanalize the URL in order to check if there have been any new discoveries to potential maliciousness.
                analysis = await session.post(f"https://www.virustotal.com/api/v3/files/{fileHash}/analyse", headers=headers)
                analysis_json = await analysis.json()

                # Wait for the analysis to complete.
                if (analysis.status == 200):
                    response = await session.get(f"https://www.virustotal.com/api/v3/analyses/{analysis_json['data']['id']}", headers=headers)
                    response_json = await response.json()
                    # Constantly ask virustotal if the analysis has finished
                    while response_json['data']['attributes']['status'] == 'queued':
                        await asyncio.sleep(2)
                        response = await session.get(f"https://www.virustotal.com/api/v3/analyses/{analysis_json['data']['id']}", headers=headers)
                        response_json = await response.json()
                    # If it finished the analysis we then move to handle the response
                    return handle_vt_analysis(response_json, file.filename, 'file')

            # If the request fails it means that there is no current analysis of the file inside of the Virustotal database
            # so we have to get our hands dirty and download the file to then upload it for it's first ever scan
            # or even better, make a bridge in between the discord file url and virustotal api, to upload the file via chunk streaming
            # which will protect the server from memory saturation and instead redirect the weight onto it's bandwidth.
            # I will be using the latter method for both heavy and light files.
            else:
                scans.info(f"Scanning file:{file.filename} with hash: {fileHash} for the first time")
                response = await session.get(file.url)
                if response.status == 200:
                    form_data = aiohttp.FormData()
                    form_data.add_field(
                        'file',
                        response.content,
                        filename=file.filename
                        )
                else:
                    raise ValueError(f"Failed to download file: {file.url} (Status: {response.status})")

                # If the file is smaller or equal then 32MB then we use the normal endpoint '/files'
                if (file.size <= 32000000):
                    scans.info(f"{file.filename} size is smaller then 32000000B. Size: {file.size}B")
                    analysis = await session.post("https://www.virustotal.com/api/v3/files", data=form_data, headers=headers)

                # If the file is between 32MB and 650MB, then we will have to ask for a custom upload url to '/files/upload_url'
                elif (file.size > 32000000 and file.size <= 650000000):
                    scans.info(f"{file.filename} size is bigger then 32000000B. Size: {file.size}B")
                    response = await session.get("https://www.virustotal.com/api/v3/files/upload_url", headers=headers)
                    response_json = await response.json()
                    upload_url = response_json['data']
                    analysis = await session.post(upload_url, data=form_data, headers=headers)

                else:
                    scans.info(f"{file.filename} size is way bigger then 650000000B. Size: {file.size}B")
                    raise ValueError(f"{file.filename} is way bigger then we can handle. Size:{file.size}B")

                if(analysis.status == 200):
                    # Wait for the analysis to complete.
                    analysis_json = await analysis.json()
                    response = await session.get(f"https://www.virustotal.com/api/v3/analyses/{analysis_json['data']['id']}", headers=headers)
                    response_json = await response.json()
                    while response_json['data']['attributes']['status'] == 'queued':
                        await asyncio.sleep(2)
                        response = await session.get(f"https://www.virustotal.com/api/v3/analyses/{analysis_json['data']['id']}", headers=headers)
                        response_json = await response.json()

                    return handle_vt_analysis(response_json, file.filename, 'file')
                else:
                    raise Exception(f"Failed the analysis with status: {analysis.status}")
    except Exception as error:
        bot.error(error)