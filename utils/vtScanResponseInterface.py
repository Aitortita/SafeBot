from typing import Dict

class Response(Dict):
    DATE_ATTRIBUTES = 'List of attributes that are dates'
    categories = 'List of categories associated with the object'
    context_attributes = 'Context attributes associated with the object'
    error = 'Error object if the object has an error'
    first_submission_date = 'Date the object was first submitted'
    from_dict = 'Method to create a new object from a dictionary'
    get = 'Method to get a value from the object'
    html_meta = 'HTML meta tags associated with the object'
    id = 'ID of the object'
    last_analysis_date = 'Date of the last analysis'
    last_analysis_results = 'Results of the last analysis'
    last_analysis_stats = 'Statistics of the last analysis'
    last_final_url = 'Final URL of the object'
    last_http_response_code = 'HTTP response code of the last analysis'
    last_http_response_content_length = 'Content length of the last analysis'
    last_http_response_content_sha256 = 'SHA-256 hash of the content of the last analysis'
    last_modification_date = 'Date the object was last modified'
    last_submission_date = 'Date the object was last submitted'
    relationships = 'Relationships associated with the object'
    reputation = 'Reputation of the object'
    set_data = 'Method to set the data of the object'
    tags = 'Tags associated with the object'
    threat_names = 'Threat names associated with the object'
    times_submitted = 'Number of times the object has been submitted'
    title = 'Title of the object'
    tld = 'Top-level domain of the object'
    to_dict = 'Method to get a dictionary representation of the object'
    total_votes = 'Total number of votes for the object'
    trackers = 'Trackers associated with the object'
    type = 'Type of the object'
    url = 'URL of the object'