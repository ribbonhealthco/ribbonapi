# ribbonapi/misc/emails.py

from typing import List, Dict, Optional, Union

from django.core.mail import EmailMultiAlternatives

import requests

from config.zepto import EMAIL_SENDER_NAME, EMAIL_API_TOKEN, EMAIL_SENDER_ADDRESS

# ZeptoMail API Configuration
ZEPTO_API_BASE_URL = "https://api.zeptomail.com/v1.1"


def send_single_email_api(
    to: List[str], 
    template_id: str, 
    vars: Optional[Dict[str, str]] = None, 
    cc: Optional[List[str]] = None, 
    bcc: Optional[List[str]] = None
) -> Union[int, None]:
    """
    Send a single email using an API with a specified template.

    Parameters:
    - to (List[str]): List of email addresses of recipients.
    - template_id (str): ID of the email template to use.
    - vars (Optional[Dict[str, str]]): Dictionary of variables for template replacement.
    - cc (Optional[List[str]]): List of email addresses to be cc'd.
    - bcc (Optional[List[str]]): List of email addresses to be bcc'd.

    Returns:
    - Union[int, None]: Status code (201) from the API response, or None if the request fails.
    """
    if vars is None:
        vars = {}
    if cc is None:
        cc = []
    if bcc is None:
        bcc = []

    # Check if 'to' is a list of strings
    if not isinstance(to, list) or not all(isinstance(email, str) for email in to):
        raise TypeError("The 'to' parameter must be a list of strings")

    # Check if 'template_id' is a string
    if not isinstance(template_id, str):
        raise TypeError("The 'template_id' parameter must be a string")

    # Check if 'vars' is a dictionary of strings or None
    if not isinstance(vars, dict):
        raise TypeError("The 'vars' parameter must be a dictionary")
    
    if vars is not None and not all(isinstance(key, str) and isinstance(value, str) for key, value in vars.items()):
        raise TypeError("The 'vars' parameter must be a dictionary with string keys and values")

    # Check if 'cc' is a list of strings or None
    if not isinstance(cc, list) or not all(isinstance(email, str) for email in cc):
        raise TypeError("The 'cc' parameter must be a list of strings or empty `list")

    # Check if 'bcc' is a list of strings or None
    if not isinstance(bcc, list) or not all(isinstance(email, str) for email in bcc):
        raise TypeError("The 'bcc' parameter must be a list of strings or empty `list`")
    
    ZEPTO_API_URL = f'{ZEPTO_API_BASE_URL}/email/template'
    headers = {
        'Authorization': EMAIL_API_TOKEN,
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    data = {
        'template_alias': template_id,
        'from': {
            'address': EMAIL_SENDER_ADDRESS,
            'name': EMAIL_SENDER_NAME
        },
        'to': [
            {'email_address': {'address': email}} for email in to
        ],
        'cc': [] if not cc else [{'email_address': {'address': email}} for email in cc],
        'bcc': [] if not bcc else [{'email_address': {'address': email}} for email in bcc],
        'merge_info': vars
    }

    try:
        response = requests.post(ZEPTO_API_URL, json=data, headers=headers)
        response.raise_for_status()
        return response.status_code
    except requests.RequestException:
        return None

def send_single_email_smtp(
    to: List[str],
    subject: str,
    plain_text: Optional[str] = None,
    html_page: Optional[str] = None,
    cc: Optional[List[str]] = None,
    bcc: Optional[List[str]] = None
) -> None:
    """
    Send a single email using SMTP with Django's EmailMultiAlternatives.

    Parameters:
    - to (List[str]): List of email addresses of recipients.
    - subject (str): Subject of the email.
    - plain_text (Optional[str]): Plain text content of the email.
    - html_page (Optional[str]): HTML content of the email.
    - cc (Optional[List[str]]): List of email addresses to be cc'd.
    - bcc (Optional[List[str]]): List of email addresses to be bcc'd.

    Returns:
    - None
    """
    if not isinstance(to, list) or not all(isinstance(email, str) for email in to):
        raise TypeError('The "to" parameter must be a list of strings')
    
    if not isinstance(subject, str):
        raise TypeError('The "subject" parameter must be a string')
    
    if plain_text is not None and not isinstance(plain_text, str):
        raise TypeError('The "plain_text" parameter must be a string')
    
    if html_page is not None and not isinstance(html_page, str):
        raise TypeError('The "html_page" parameter must be a string')
    
    if cc is not None and (not isinstance(cc, list) or not all(isinstance(email, str) for email in cc)):
        raise TypeError('The "cc" parameter must be a list of strings or None')
    
    if bcc is not None and (not isinstance(bcc, list) or not all(isinstance(email, str) for email in bcc)):
        raise TypeError('The "bcc" parameter must be a list of strings or None')

    if not plain_text and not html_page:
        raise ValueError('Either plain_text or html_page must be provided')

    email = EmailMultiAlternatives(
        subject, plain_text, EMAIL_SENDER_ADDRESS, to=to, cc=cc, bcc=bcc)
    
    if html_page:
        email.attach_alternative(html_page, 'text/html')
    
    print(email.connection)
    email.send()

def send_email(
    to: List[str], 
    subject: str, 
    template_id: Optional[str] = None, 
    vars: Optional[Dict[str, str]] = None, 
    plain_text: Optional[str] = None, 
    html_page: Optional[str] = None, 
    cc: Optional[List[str]] = None, 
    bcc: Optional[List[str]] = None
) -> Dict[str, Union[str, int]]:
    """
    Post an email to be sent using ZeptoMail API with SMTP fallback.

    Note: though sending mails via API should always work, if you anticipate that
    APIs may fail, you must prepare email content before hand in plain text and HTML.

    Parameters:
    - to (List[str]): List of email addresses of recipients.
    - subject (str): Subject of the email.
    - template_id (Optional[str]): ID of the email template.
    - vars (Optional[Dict[str, str]]): Dictionary of variables to be used in the email template.
    - plain_text (Optional[str]): Plain text content of the email.
    - html_page (Optional[str]): HTML content of the email.
    - cc (Optional[List[str]]): List of email addresses to be cc'd.
    - bcc (Optional[List[str]]): List of email addresses to be bcc'd.

    Returns:
    - Dict[str, Union[str, int]]: Response containing the status, code, and message of sending the email.
    """
    # Type checks
    if not isinstance(to, list) or not all(isinstance(email, str) for email in to):
        raise TypeError('The "to" parameter must be a list of strings')
    
    if not isinstance(subject, str):
        raise TypeError('The "subject" parameter must be a string')
    
    if template_id is not None and not isinstance(template_id, str):
        raise TypeError('The "template_id" parameter must be a string')

    if vars is not None and (not isinstance(vars, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in vars.items())):
        raise TypeError('The "vars" parameter must be a dictionary with string keys and string values')

    if plain_text is not None and not isinstance(plain_text, str):
        raise TypeError('The "plain_text" parameter must be a string')
    
    if html_page is not None and not isinstance(html_page, str):
        raise TypeError('The "html_page" parameter must be a string')
    
    if cc is not None and (not isinstance(cc, list) or not all(isinstance(email, str) for email in cc)):
        raise TypeError('The "cc" parameter must be a list of strings or None')
    
    if bcc is not None and (not isinstance(bcc, list) or not all(isinstance(email, str) for email in bcc)):
        raise TypeError('The "bcc" parameter must be a list of strings or None')

    # Default values
    if vars is None:
        vars = {}
    if cc is None:
        cc = []
    if bcc is None:
        bcc = []

    # Try sending via ZeptoMail API
    # status_code = send_single_email_api(to, template_id, vars, cc, bcc)
    status_code = None
    
    # Fallback to SMTP if API fails
    if not status_code or status_code != 201:
        send_single_email_smtp(to, subject, plain_text, html_page, cc, bcc)
