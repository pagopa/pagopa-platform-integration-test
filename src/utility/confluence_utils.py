from requests.models import HTTPBasicAuth
import os
import requests
import json


headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
PAGE_BODY_FORMAT = '?body-format=storage'


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
def upload_page_content(existing_page, data, auth, url='https://pagopa.atlassian.net/wiki/api/v2/pages/'):  
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

        response = requests.request(
        "PUT",
        url=url + existing_page['id'],
        data=payload,
        headers=headers,
        auth=auth
        )
        response.raise_for_status()
    except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as e:
        raise Exception(f"Failed to update confluence page content for page id: {existing_page['id']}. Error: {str(e)}")

    print(f"[INFO][updateConfluencePageContent] Successfully updated confluence page content for page id: {existing_page['id']}")



def get_existing_page_content(fileIn,confluence_url: str = 'https://pagopa.atlassian.net/wiki/api/v2/pages/', page_id: str = None, auth_obj: HTTPBasicAuth = None):
    # retrieving the existing confluence page content using the page id from the first line of the feature file
    try:
        url = f'{confluence_url}{page_id}'
        response = requests.request(
            "GET",
            url=url + PAGE_BODY_FORMAT,
            headers=headers,
            auth=auth_obj
        )
        response.raise_for_status()
        print(f"[INFO][getConfluencePageContent] Successfully retrieved content for confluence page id: {page_id}")
    except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as e:
        raise Exception(f"Failed to get content for confluence page id: {page_id}. Error: {str(e)}")
    
    return response.json()



def create_confluence_page(page_content,config, confluence_url: str = 'https://pagopa.atlassian.net/wiki/api/v2/pages/', auth_obj: HTTPBasicAuth = None, page_title: str = None, parent_key: str = None):
    """Create a Confluence page.

    Parameters are generic so this function can be moved to a utility class later.
    If `auth_obj` is not provided, the function will try to read `CONFLUENCE_EMAIL` and
    `CONFLUENCE_KEY` from the environment and build an `HTTPBasicAuth` instance.
    """
    try:
        parent_id = config.get('parent_id')
    except Exception as e:
        raise RuntimeError(f"Failed to get parent_id from config. Error: {str(e)}")

    try:
        # parent config key: all parts except last joined by '-'; fallback to folder_name
        payload = {
            "spaceId": "2561638408",
            "status": "current",
            "title": page_title,
            "parentId": parent_id,
            "body": {
                "representation": "storage",
                "value": page_content
            },
        }

        response = requests.post(confluence_url, json=payload, headers=headers, auth=auth_obj)
        response.raise_for_status()
        print(f"[INFO][create_confluence_page] Successfully created page (status={response.status_code})")
        return response.json()
    except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as e:
        raise Exception(f"Failed to create confluence page. Error: {str(e)}")
    except Exception as e:
        raise