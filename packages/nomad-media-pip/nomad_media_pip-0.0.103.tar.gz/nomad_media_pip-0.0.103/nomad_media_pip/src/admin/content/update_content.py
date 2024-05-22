from nomad_media_pip.src.exceptions.api_exception_handler import _api_exception_handler
from nomad_media_pip.src.admin.content.get_content import _get_content

import json, requests
from deepdiff import DeepDiff

def _update_content(AUTH_TOKEN, URL, ID, CONTENT_DEFINITION_ID, PROPERTIES, 
                    LANGUAGE_ID, DEBUG):
    # Create header for the request
    if not AUTH_TOKEN:
        raise Exception("Authorization token not found")
  
    API_URL = f"{URL}/api/content/{ID}"
    
    HEADERS = {
      "Content-Type": "application/json",
      "Authorization": "Bearer " + AUTH_TOKEN
    }

    try:
        BODY = _get_content(AUTH_TOKEN, URL, ID, CONTENT_DEFINITION_ID, None, DEBUG)

        if (BODY["contentDefinitionId"] != CONTENT_DEFINITION_ID): BODY["contentDefinitionId"] = CONTENT_DEFINITION_ID
        if (BODY.get("languageId") != LANGUAGE_ID): BODY["languageId"] = LANGUAGE_ID
        if (BODY["contentId"] != ID): BODY["contentId"] = ID

        _update_properties(BODY, PROPERTIES)

    except:
        BODY = {
            "contentDefinitionId": CONTENT_DEFINITION_ID,
            "contentId": ID,
            "languageId": LANGUAGE_ID,
            "properties": PROPERTIES
        }

    if DEBUG:
        print(f"URL: {API_URL},\nMETHOD: POST,\nBODY: {json.dumps(BODY, indent=4)}")

    try:
        # Send POST request
        RESPONSE = requests.put(API_URL, headers=HEADERS, data=json.dumps(BODY))

        # Check for success
        if (not RESPONSE.ok):
            raise Exception()
        
        # Get the response
        ID = RESPONSE.json()

        # Return the ID
        return ID
    
    except:
        _api_exception_handler(RESPONSE, "Update Content failed")

def _update_properties(body, properties):
    for property, value in properties.items():
        if isinstance(value, list):
            for i in range(len(value)):
                if DeepDiff(body['properties'][property][i], value[i]):
                    body['properties'][property][i] = value[i]
        elif isinstance(value, dict):
            if DeepDiff(body['properties'][property], value):
                body['properties'][property] = value
        elif body['properties'].get(property) != value:
            body['properties'][property] = value

