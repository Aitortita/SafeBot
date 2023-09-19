import aiohttp
import asyncio
import settings
from utils.functions.urlIdGenerator import url_id_generator
from utils.functions.handleVtAnalysis import handle_vt_analysis

headers = {
    "accept": "application/json",
    "X-Apikey": settings.VIRUSTOTAL_API_KEY
}

queued: str = 'queued'

async def scan_url(url: str) -> dict:
        """
        Scan a single URL and return the results.

        Args:
            url: The URL id to scan.

        Returns:
            A Dict containing the results of the scan.
        """
        url_id = url_id_generator(url)
        try:
            async with aiohttp.ClientSession() as session:
                # Make an asynchronous request to VirusTotal to check if there is an analysis of the URL.
                response = await session.get(f"https://www.virustotal.com/api/v3/urls/{url_id}", headers=headers)

                if(response.status == 200):
                    # If the request was successful it means that an already made analysis exists, so we need to ask VirusTotal to reanalize the URL in order to check if there have been any new discoveries to potential maliciousness.
                    analysis = await session.post(f"https://www.virustotal.com/api/v3/urls/{url_id}/analyse", headers=headers)

                    # Wait for the analysis to complete.
                    if (analysis.status == 200):
                        analysis_json = await analysis.json()
                        response = await session.get(f"https://www.virustotal.com/api/v3/analyses/{analysis_json['data']['id']}", headers=headers)
                        response_json = await response.json()
                        while response_json['data']['attributes']['status'] == queued:
                            await asyncio.sleep(2)
                            response = await session.get(f"https://www.virustotal.com/api/v3/analyses/{analysis_json['data']['id']}", headers=headers)
                            
                        return handle_vt_analysis(response_json)
                # If the request fails it means that there is no current analysis of the URL inside of VirusTotal Database
                else:
                    # Ask for a new analysis of the URL
                    analysis = await session.post("https://www.virustotal.com/api/v3/urls", data={ "url": url }, headers={
                        "accept": "application/json",
                        "X-Apikey": settings.VIRUSTOTAL_API_KEY,
                        "content-type": "application/x-www-form-urlencoded"
                    })

                    if(analysis.status == 200):
                        analysis_json = await analysis.json()
                        # Wait for the analysis to complete.
                        response = await session.get(f"https://www.virustotal.com/api/v3/analyses/{analysis_json['data']['id']}", headers=headers)
                        response_json = await response.json()
                        while response_json['data']['attributes']['status'] == queued:
                            await asyncio.sleep(2)
                            response = await session.get(f"https://www.virustotal.com/api/v3/analyses/{analysis_json['data']['id']}", headers=headers)

                        handle_vt_analysis(response_json)
        except Exception as error:
            print(error)