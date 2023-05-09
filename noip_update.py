import base64
from urllib.request import Request, urlopen


def create_update_url(hostname, new_ip):
    return "https://dynupdate.no-ip.com/nic/update?hostname={}&myip={}"\
        .format(hostname, new_ip)


def base64_encode_auth_string(username, password):
    return base64.b64encode("{}:{}".format(username, password).encode())


def send_update_request(username, password, hostname, user_agent, new_ip):
    request_url = create_update_url(hostname, new_ip)
    encoded_auth_string = base64_encode_auth_string(username, password)
    headers = {
        "Host": "dynupdate.no-ip.com",
        "Connection": "keep-alive",
        "Accept": "*/*",
        "Authorization": "Basic {}".format(encoded_auth_string),
        "User-Agent": "{}".format(user_agent),
        "Content-Type": "text/plain; charset=UTF-8"
    }
    request = Request(request_url, headers=headers)
    with urlopen(request) as response:
        return response.read()
