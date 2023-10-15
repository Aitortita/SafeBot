import json

malicious: str = 'malicious'
clean: str = 'clean'

def handle_vt_analysis(analysis: json) -> dict:
    # Initialize a dictionary to store the antivirus flags.
    antivirusFlags = {}
    # Check if the analysis found any malicious results.
    for antivirus, detection_result in analysis['data']['attributes']['results'].items():
        if detection_result["result"] == "phishing" or detection_result["result"] == "malicious":
            antivirusFlags[antivirus] = detection_result["result"]

    # If any malicious results were found, return an error message.
    if len(antivirusFlags) >= 1:
        return {
            'status': malicious,
            'message': f"The url '{analysis['meta']['url_info']['url']}' is malicious, don't click it.\nHere is a list of antiviruses that listed it as malicious: ```json\n{json.dumps(antivirusFlags, indent=3)}\n```"
        }

    # Otherwise, return a success message.
    else:
        return {
            'status': clean,
            'message': f"The url '{analysis['meta']['url_info']['url']}' is safe"
        }