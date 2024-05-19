from datetime import datetime

def type_pw(value, valueid):
    """
    Trích xuất mật khẩu từ một chuỗi dữ liệu dựa trên ID người dùng.

    Args:
        value (str): Chuỗi dữ liệu chứa ID và mật khẩu.
        valueid (str): ID người dùng để tìm mật khẩu.

    Returns:
        str: Mật khẩu tương ứng với ID người dùng.
    """
    tokens = value.split("|")
    try:
        index = tokens.index(valueid)
        return tokens[index + 1] if index + 1 < len(tokens) else None
    except ValueError:
        return None

def type_pwemail(value, valuemail):
    """
    Trích xuất mật khẩu email từ một chuỗi dữ liệu dựa trên email.

    Args:
        value (str): Chuỗi dữ liệu chứa email và mật khẩu.
        valuemail (str): Email để tìm mật khẩu.

    Returns:
        str: Mật khẩu tương ứng với email.
    """
    tokens = value.split("|")
    try:
        index = tokens.index(valuemail)
        return tokens[index + 1] if index + 1 < len(tokens) else None
    except ValueError:
        return None

def headers():
    """
    Tạo và trả về một từ điển chứa các header HTTP mặc định.

    Returns:
        dict: Một từ điển chứa các header HTTP.
    """
    return {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/x-www-form-urlencoded",
        "X-Do-Not-Track": "1",
        "sec-ch-ua-mobile": "?0",
        "Connection": "keep-alive",
        "DNT": "1",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "upgrade-insecure-requests": "1",
        "x-requested-with": "XMLHttpRequest",
        "x-response-format": "JSONStream",
        "viewport-width": "934",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    }

def type_emailr(value):
    """
    Kiểm tra xem chuỗi có chứa chỉ các ký tự chữ cái không.

    Args:
        value (str): Chuỗi cần kiểm tra.

    Returns:
        bool: True nếu chuỗi chỉ chứa ký tự chữ cái, ngược lại False.
    """
    return all(x.isalpha() for x in value)

def dict_typ():
    """
    Tạo và trả về một từ điển chứa các khóa mặc định cho dữ liệu người dùng.

    Returns:
        dict: Một từ điển chứa các khóa mặc định cho dữ liệu người dùng.
    """
    return {
        "c_user": "",
        "password": "",
        "code": "",
        "email": "",
        "passemail": "",
        "user-agent": "",
        "cookie": "",
        "fb_dtsg": "",
        "id": "",
        "text": "",
        "proxy": "",
        "reaction": "",
        "access_token": "",
        "business": "",
        "attent_id": "",
        "feeling": "",
        "headers": headers()
    }
