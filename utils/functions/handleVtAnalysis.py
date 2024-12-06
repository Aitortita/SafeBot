import json
from logging import getLogger
logger = getLogger("bot")

def handle_vt_analysis(analysis: json, name: str, type: str) -> dict:
    """
    Handles the Virustotal analysis response, filtering every malicious/suspicious
    evaluations and returning a dict containing the veredict in the form of a status and message 

    Args:
        analysis: the analysis response in the form of a json.
        name: the name of the file/url in the form of a string.
        type: the type of the object scanned, in the form of a url or a file.

    Returns:
        A Dict containing the final result of the Safebot scan.
    """
    # Initialize a dictionary to store the antivirus flags.
    antivirusFlags = {}
    # Check if the analysis found any malicious results.
    for antivirus, evaluation in analysis['data']['attributes']['results'].items():
        if evaluation["category"] in ["malicious", "suspicious"]:
            antivirusFlags[antivirus] = evaluation["result"]

    # If any malicious results were found, return a message containing the antiviruses that flagged it as malicious and their results.
    if len(antivirusFlags) >= 1:
        return {
            'status': 'malicious',
            'message': f"The {type} '{name}' is malicious.\nHere is a list of antiviruses that flagged it as malicious: ```json\n{json.dumps(antivirusFlags, indent=3)}\n```"
        }

    # Otherwise, return a clean message.
    else:
        return {
            'status': 'clean',
            'message': f"The {type} '{name}' is safe"
        }