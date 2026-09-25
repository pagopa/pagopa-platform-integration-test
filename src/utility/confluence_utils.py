from requests.models import HTTPBasicAuth
import os
import requests
import json


headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
PAGE_BODY_FORMAT = '?body-format=storage'
CONFLUENCE_BASE_URL = 'https://pagopa.atlassian.net/wiki/api/v2/{context}'
PAGOPA_QA_SPACE_ID = '2561638408'
PAGES = 'pages'
FOLDERS = 'folders'
DESCENDANTS = 'descendants'

def create_confluence_auth():
    """Create an HTTPBasicAuth object for Confluence API authentication.

    This function reads the `CONFLUENCE_EMAIL` and `CONFLUENCE_KEY` environment variables
    to create an `HTTPBasicAuth` instance. If either of the environment variables is not set,
    it raises a `RuntimeError`.

    Returns:
        HTTPBasicAuth: An instance of HTTPBasicAuth for Confluence API authentication.
    Raises:
        RuntimeError: If either `CONFLUENCE_EMAIL` or `CONFLUENCE_KEY` is not set in the environment.
    """
    confluence_email = os.getenv('CONFLUENCE_EMAIL')
    confluence_key = os.getenv('CONFLUENCE_KEY')

    if not confluence_email or not confluence_key:
        raise RuntimeError("Both CONFLUENCE_EMAIL and CONFLUENCE_KEY environment variables must be set.")

    return HTTPBasicAuth(confluence_email, confluence_key)


# Function used to update the existing confluence page content
def upload_page_content(existing_page, data, auth, confluence_url=CONFLUENCE_BASE_URL):  
    
    """
    Update the content of an existing Confluence page.

    Parameters:
        existing_page (dict): The existing Confluence page data.
        data (str): The new content to update the page with.
        auth (HTTPBasicAuth): The authentication object for Confluence API.
        confluence_url (str): The base URL for the Confluence API pages endpoint.
                              Defaults to CONFLUENCE_BASE_URL.
    
    
    
    raises:
        Exception: If the request to update the page content fails.
    """
    
    try:
        payload = json.dumps( {
        "id": existing_page['id'],
        "status": "current",
        "title": existing_page['title'],
        "body": {
        "representation": "storage",
        "value": data
        },
        "version": {
        "number": existing_page['version']['number'] + 1,
        "message": "Updated feature file content via GitHub Action"
        }
        })
        url = confluence_url.replace("{context}", PAGES)
        response = requests.put(url=url + existing_page['id'],data=payload,headers=headers,auth=auth)
        response.raise_for_status()
    except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as e:
        raise Exception(f"Failed to update confluence page content for page id: {existing_page['id']}. Error: {str(e)}")

    print(f"[INFO][updateConfluencePageContent] Successfully updated confluence page content for page id: {existing_page['id']}")



def get_existing_page_content(confluence_url: str = CONFLUENCE_BASE_URL, page_id: str = None, auth_obj: HTTPBasicAuth = None):
    """
    Retrieve the content of an existing Confluence page.

    Parameters:
        confluence_url (str): The base URL for the Confluence API pages endpoint.
                              Defaults to CONFLUENCE_BASE_URL.
        page_id (str): The ID of the Confluence page to retrieve.
        auth_obj (HTTPBasicAuth): The authentication object for Confluence API.
        
        The default value for the confluence_url parameter is "https://pagopa.atlassian.net/wiki/api/v2/pages/".

    Returns:
        dict: The JSON response containing the Confluence page content.

    Raises:
        Exception: If the request to retrieve the page content fails.
    """
    
   
   
    # retrieving the existing confluence page content using the page id from the first line of the feature file
    try:
        url = f'{confluence_url.replace("{context}", PAGES)}{page_id}'
        response = requests.get(url=url + PAGE_BODY_FORMAT,headers=headers,auth=auth_obj
        )
        response.raise_for_status()
        print(f"[INFO][getConfluencePageContent] Successfully retrieved content for confluence page id: {page_id}")
    except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as e:
        raise Exception(f"Failed to get content for confluence page id: {page_id}. Error: {str(e)}")
    
    return response.json()



def create_confluence_page(page_content,parent_id, confluence_url: str = CONFLUENCE_BASE_URL, auth_obj: HTTPBasicAuth = None, page_title: str = None):
    """Create a Confluence page.
    
    Parameters:
        page_content (str): The content of the Confluence page to create.
        config (dict): The configuration dictionary containing the parent_id.
        confluence_url (str): The base URL for the Confluence API pages endpoint.
                              Defaults to CONFLUENCE_BASE_URL.
        auth_obj (HTTPBasicAuth): The authentication object for Confluence API.
        page_title (str): The title of the Confluence page to create.
        parent_key (str): The key of the parent page under which to create the new page.
        
         The default value for the confluence_url parameter is "https://pagopa.atlassian.net/wiki/api/v2/pages/".

    Returns:
        dict: The JSON response containing the created Confluence page details.

    Raises:
        Exception: If the request to create the page fails or if any other error occurs during the process.

    """
   
    try:
        # parent config key: all parts except last joined by '-'; fallback to folder_name
        payload = {
            "spaceId": PAGOPA_QA_SPACE_ID,
            "status": "current",
            "title": page_title,
            "parentId": parent_id,
            "body": {
                "representation": "storage",
                "value": page_content
            },
        }
        url= confluence_url.replace("{context}", PAGES)
        response = requests.post(url, json=payload, headers=headers, auth=auth_obj)
        response.raise_for_status()
        print(f"[INFO][create_confluence_page] Successfully created page (status={response.status_code})")
        return response.json()
    except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as e:
        raise Exception(f"Failed to create confluence page. Error: {str(e)}")
    except Exception as e:
        raise
    
    
def get_descendants(config,confluence_auth, confluence_url: str = CONFLUENCE_BASE_URL):
        """
        Get the descendants of a Confluence page.

        Parameters:
            config (dict): The configuration dictionary containing the parent_id.
            confluence_auth (HTTPBasicAuth): The authentication object for Confluence API.

        Returns:
            dict: The JSON response containing the descendants of the Confluence page.

        Raises:
            Exception: If the request to get the descendants fails or if any other error occurs during the process.

        """
        try:
            parent_id = config.get('parent_id')
        except Exception as e:
            raise RuntimeError(f"Failed to get parent_id from config. Error: {str(e)}")
        
        try:
            # parent config key: all parts except last joined by '-'; fallback to folder_name
            url = CONFLUENCE_BASE_URL.replace("{context}", FOLDERS + f"/{parent_id}/" + DESCENDANTS)
            response = requests.get(url, headers=headers, auth=confluence_auth)
            response.raise_for_status()
            print(f"[INFO][get_descendants] Successfully retrieved descendants (status={response.status_code})")
            return response.json()
        except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as e:
            raise Exception(f"Failed to get descendants of confluence page. Error: {str(e)}")
        except Exception as e:
            raise
        
def create_confluence_folder(config,title, confluence_auth, confluence_url: str = CONFLUENCE_BASE_URL):
    try:
        try:
            parent_id = config.get('parent_id')
        except Exception as e:
            raise RuntimeError(f"Failed to get parent_id from config. Error: {str(e)}")

        payload = json.dumps({
            "spaceId": PAGOPA_QA_SPACE_ID,
            "title": title,
            "parentId": parent_id
        })

        url = confluence_url.replace("{context}", FOLDERS)
        response = requests.post(url,data=payload,headers=headers,auth=confluence_auth)
        response.raise_for_status()
        print(f"[INFO][create_confluence_folder] Successfully created folder (status={response.status_code})")
        return response.json()
    except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as e:
        raise Exception(f"Failed to create confluence folder. Error: {str(e)}")
    except Exception as e:
        raise