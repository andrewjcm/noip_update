import urllib.request
import os
from dotenv import load_dotenv
from noip_update import send_update_request

load_dotenv()


def get_external_ip():
    return urllib.request.urlopen(os.getenv("WHOAMI_URL")).read().decode("utf8")


def read_noip():
    try:
        with open("noip.txt", "r") as file:
            return file.read()
    except IOError:
        return None


def write_noip(ip):
    with open("noip.txt", "w") as file:
        file.write(ip)


def update_noip(new_ip):
    send_update_request(
        os.getenv("BASE_64_AUTH"),
        os.getenv("HOSTNAME"),
        os.getenv("USER_AGENT"),
        new_ip
    )


def main():
    current_ip = read_noip()
    new_ip = get_external_ip()
    if current_ip != new_ip:
        print(update_noip(new_ip))
        write_noip(new_ip)


if __name__ == "__main__":
    main()
