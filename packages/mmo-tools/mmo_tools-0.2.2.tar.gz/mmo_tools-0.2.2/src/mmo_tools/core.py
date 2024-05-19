import os
import re
import requests
from . import utils

def convert_data(file) -> list:

    """
    Tele : t.me/im_dlam
    Converts data from a file into a structured format.

    Returns:
        list: A list of dictionaries containing user data.
    """
    try:
        with open(file, "r", encoding="UTF-8") as f:
            data_lines = f.readlines()
    except Exception as e:
        return str(e)
    
    data = []
    for line in data_lines:
        line = line.strip()
        if not line:
            continue
        
        user_data = parse_user_data(line)
        data.append(user_data)
    
    return data

def parse_user_data(line: str) -> dict:
    """
    Parses a single line of user data into a dictionary.

    Args:
        line (str): A single line of user data.

    Returns:
        dict: Parsed user data.
    """
    rp = utils.dict_typ()
    user = extract_user(line)
    rp["c_user"] = user

    password = utils.type_pw(value=line, valueid=user)
    if password:
        rp["password"] = password

    tokens = line.split("|")
    for token in tokens:
        token = token.strip()
        update_user_data(rp, token, line)

    return rp

def extract_user(line: str) -> str:
    """
    Extracts the user ID from a line.

    Args:
        line (str): A single line of user data.

    Returns:
        str: Extracted user ID.
    """
    if "c_user" in line and "i_user" not in line:
        return line.split("c_user=")[1].split(";")[0]
    elif "i_user" in line:
        return line.split("i_user=")[1].split(";")[0]
    return ""

def update_user_data(rp: dict, token: str, line: str):
    """
    Updates the user data dictionary with information from the token.

    Args:
        rp (dict): The user data dictionary.
        token (str): The token to parse.
        line (str): The original line of user data.
    """
    if "NA" in token and ":" in token:
        rp["fb_dtsg"] = token
    if "c_user" in token or "i_user" in token:
        rp["cookie"] = token
    if any(agent in token for agent in ["Mozilla", "Chrome", "Safari", "AppleWebKit"]):
        rp["user-agent"] = token
    if len(token) > 150 and '=' not in token:
        rp['access_token'] = token
    if len(token.split(':')) in [2, 4] or 'http://' in token:
        rp['proxy'] = token
    if "c_user" not in token and 32 <= len(token) <= 40 and "@" not in token:
        rp['code'] = token
    if "@" in token:
        email = re.search(r'@(.*)\.', token)
        if email and utils.type_emailr(email.group(1)):
            rp['email'] = token
            password_email = utils.type_pw(value=line, valueid=email.group(1))
            if password_email:
                rp['passemail'] = password_email

def convert_headers(header_str: str) -> dict:
    """
    Converts a string of headers into a dictionary.

    Returns:
        dict: A dictionary of headers.
    """
    headers = {}
    headers , check , name = {} , 0 , ""
    if "\n" not in header_str:
        print("""
        Headers are not in the correct format.
              Example 1: 

                   Accept:
*/*
              Content-Type:
application/x-www-form-urlencoded
              

              Example 2 :

                   Accept:*/*,
                   Content-Type:application/x-www-form-urlencoded
              
""")
    header_str =  header_str.replace('\n','|').replace('"','`').replace('://','(^)').split('|')
    try:
        for temp in header_str:
            if temp[-1:] == ':':
                name = temp[:-1].replace('\n','').replace('`','"').replace('(^)','://')
                headers.update({name:""})
                check = 1
            if temp[-1:] != ':' and check:
                headers.update({name:temp.replace('\n','').replace('`','"').replace('(^)','://')})
                check = 0
    except Exception as error:
        print(error)
        return headers
    return headers

def convert_proxy(proxy_str: str) -> dict:
    """
    Converts a proxy string into a dictionary format.

    Returns:
        dict: A dictionary containing proxy information.
    """
    proxy_dict = {}
    try:
        if "@" in proxy_str or len(proxy_str.split(":")) in [2, 4]:
            proxy_dict = {
                "https": f"http://{proxy_str}",
                "http": f"http://{proxy_str}"
            }
        else:
            ip, port, user, pass_proxy = proxy_str.split(":")
            proxy_dict = {
                "https": f"http://{user}:{pass_proxy}@{ip}:{port}",
                "http": f"http://{user}:{pass_proxy}@{ip}:{port}"
            }
    except ValueError:
        proxy_dict = {
            "https": f"http://{proxy_str}",
            "http": f"http://{proxy_str}"
        }
    return proxy_dict

def cookie_confirm_auth_2fa(session: requests.Session, code: str, fb_dtsg: str) -> bool:
    """
    Requests confirmation for 2FA.

    Args:
        session (requests.Session): The Facebook session.
        code (str): The 8-digit code.
        fb_dtsg (str): The FB token.

    Returns:
        bool: True if confirmation is successful, otherwise False.
    """
    try:
        response = session.post(
            "https://business.facebook.com/security/twofactor/reauth/enter/",
            data={
                "approvals_code": code,
                "save_device": "true",
                "__a": "1",
                "fb_dtsg": fb_dtsg
            },
            timeout=60
        )
        return '"codeConfirmed":true' in response.text
    except requests.RequestException as e:
        print(f"Error confirming 2FA: {e}")
        return False

def check_facebook_account(fbid: str) -> bool:
    """
    Checks if a Facebook account is live or not.

    Args:
        fbid (str): The Facebook ID.

    Returns:
        bool: True if the account is live, otherwise False.
    """
    try:
        response = requests.get(f'https://graph.facebook.com/{fbid}/picture?redirect=0')
        data = response.json()
        url = data.get('data', {}).get('url', '')
        return len(url) >= 150
    except (requests.RequestException, KeyError) as e:
        print(f"Error checking Facebook account: {e}")
        return False
