from urllib.request import Request, urlopen

import requests
from requests import HTTPError


def create_update_url(hostname, new_ip):
    return "https://dynupdate.no-ip.com/nic/update?hostname={}&myip={}"\
        .format(hostname, new_ip)


def send_update_request(auth, hostname, user_agent, new_ip):
    request_url = create_update_url(hostname, new_ip)
    headers = {
        "Authorization": "Basic {}".format(auth),
        "User-Agent": "{}".format(user_agent),
    }
    response = requests.get(request_url, headers=headers)
    if response.status_code == 401 and "badauth" in response.text:
        raise HTTPError("Invalid username password combination.")
    elif response.status_code == 200:
        if "good" in response.text:
            return "DNS hostname update successful. New IP: {}".format(new_ip)
        elif "nochg" in response.text:
            return "IP address is current, no update performed."
    else:
        if "nohost" in response.text:
            raise HTTPError("Hostname supplied does not exist under specified account")
        elif "badagent" in response.text:
            raise HTTPError("	Client disabled")
        elif "!donator" in response.text:
            raise HTTPError("An update request was sent, including a feature that is not available to that particular user such as offline options.")
        elif "abuse" in response.text:
            raise HTTPError("Username is blocked due to abuse")
        elif "911" in response.text:
            raise HTTPError("A fatal error on our side such as a database outage. Retry the update no sooner than 30 minutes. ")

