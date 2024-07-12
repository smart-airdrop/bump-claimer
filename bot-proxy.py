import os
import sys
import time
import requests
from requests.auth import HTTPProxyAuth
from colorama import *
from datetime import datetime
import json
import random
import brotli

red = Fore.LIGHTRED_EX
yellow = Fore.LIGHTYELLOW_EX
green = Fore.LIGHTGREEN_EX
black = Fore.LIGHTBLACK_EX
blue = Fore.LIGHTBLUE_EX
white = Fore.LIGHTWHITE_EX
reset = Style.RESET_ALL

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.realpath(__file__))

# Construct the full paths to the files
data_file = os.path.join(script_dir, "data-proxy.json")


class BUMP:
    def __init__(self):
        self.line = white + "~" * 50

        self.banner = f"""
        {blue}Smart Airdrop {white}Bump Auto Claimer
        t.me/smartairdrop2120
        
        """

    # Clear the terminal
    def clear_terminal(self):
        # For Windows
        if os.name == "nt":
            _ = os.system("cls")
        # For macOS and Linux
        else:
            _ = os.system("clear")

    def headers(self, auth_data):
        return {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9",
            "Authorization": f"Bearer {auth_data}",
            "Origin": "https://mmbump.pro",
            "Pragma": "no-cache",
            "Priority": "u=1, i",
            "Referer": "https://mmbump.pro/",
            "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        }

    def proxies(self, proxy_info):
        return {"http": f"{proxy_info}", "https": f"{proxy_info}"}

    def check_ip(self, proxy_info):
        url = "https://api.ipify.org?format=json"

        proxies = self.proxies(proxy_info=proxy_info)

        # Parse the proxy credentials if present
        if "@" in proxy_info:
            proxy_credentials = proxy_info.split("@")[0]
            proxy_user = proxy_credentials.split(":")[1]
            proxy_pass = proxy_credentials.split(":")[2]
            auth = HTTPProxyAuth(proxy_user, proxy_pass)
        else:
            auth = None

        try:
            response = requests.get(url=url, proxies=proxies, auth=auth)
            response.raise_for_status()  # Raises an error for bad status codes
            return response.json().get("ip")
        except requests.exceptions.RequestException as e:
            print(f"IP check failed: {e}")
            return None

    def auth_user(self, data, proxy_info):
        url = "https://api.mmbump.pro/v1/loginJwt"

        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9",
            "Origin": "https://mmbump.pro",
            "Pragma": "no-cache",
            "Priority": "u=1, i",
            "Referer": "https://mmbump.pro/",
            "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        }

        payload = {"initData": f"{data}"}

        payload = json.dumps(payload)

        headers["Content-Length"] = str(len(payload))
        headers["Content-Type"] = "application/json"

        proxies = self.proxies(proxy_info=proxy_info)

        response = requests.post(
            url=url, headers=headers, data=payload, proxies=proxies
        )

        return response

    def farming(self, auth_data, proxy_info):
        url = "https://api.mmbump.pro/v1/farming"

        headers = self.headers(auth_data=auth_data)

        proxies = self.proxies(proxy_info=proxy_info)

        response = requests.post(url=url, headers=headers, proxies=proxies)

        return response

    def start_farming(self, auth_data, proxy_info):
        url = "https://api.mmbump.pro/v1/farming/start"

        headers = self.headers(auth_data=auth_data)

        payload = {"status": "inProgress"}

        proxies = self.proxies(proxy_info=proxy_info)

        response = requests.post(
            url=url, headers=headers, data=payload, proxies=proxies
        )

        return response

    def finish_farming(self, auth_data, tap, proxy_info):
        url = "https://api.mmbump.pro/v1/farming/finish"

        headers = self.headers(auth_data=auth_data)

        payload = {"tapCount": tap}

        proxies = self.proxies(proxy_info=proxy_info)

        response = requests.post(
            url=url, headers=headers, data=payload, proxies=proxies
        )

        return response

    def check_in(self, auth_data, proxy_info):
        url = "https://api.mmbump.pro/v1/grant-day/claim"

        headers = self.headers(auth_data=auth_data)

        proxies = self.proxies(proxy_info=proxy_info)

        response = requests.post(url=url, headers=headers, data={}, proxies=proxies)

        return response

    def ref_claim(self, auth_data, proxy_info):
        url = "https://api.mmbump.pro/v1/friends/claim"

        headers = self.headers(auth_data=auth_data)

        proxies = self.proxies(proxy_info=proxy_info)

        response = requests.post(url=url, headers=headers, proxies=proxies)

        return response

    def check_task(self, auth_data, proxy_info):
        url = "https://api.mmbump.pro/v1/task-list"

        headers = self.headers(auth_data=auth_data)

        proxies = self.proxies(proxy_info=proxy_info)

        response = requests.post(url=url, headers=headers, proxies=proxies)

        return response

    def complete_task(self, auth_data, task_id, proxy_info):
        url = "https://api.mmbump.pro/v1/task-list/complete"

        headers = self.headers(auth_data=auth_data)

        payload = {"id": task_id}

        proxies = self.proxies(proxy_info=proxy_info)

        response = requests.post(
            url=url, headers=headers, data=payload, proxies=proxies
        )

        return response

    def log(self, msg):
        now = datetime.now().isoformat(" ").split(".")[0]
        print(f"{black}[{now}]{reset} {msg}{reset}")

    def parse_proxy_info(self, proxy_info):
        try:
            stripped_url = proxy_info.split("://", 1)[-1]
            credentials, endpoint = stripped_url.split("@", 1)
            user_name, password = credentials.split(":", 1)
            ip, port = endpoint.split(":", 1)
            return {"user_name": user_name, "pass": password, "ip": ip, "port": port}
        except:
            return None

    def main(self):
        while True:
            self.clear_terminal()
            print(self.banner)
            accounts = json.load(open(data_file, "r"))["accounts"]
            num_acc = len(accounts)
            self.log(self.line)
            self.log(f"{green}Numer of account: {white}{num_acc}")
            for no, account in enumerate(accounts):
                self.log(self.line)
                self.log(f"{green}Account number: {white}{no+1}/{num_acc}")
                data = account["acc_info"]
                proxy_info = account["proxy_info"]
                parsed_proxy_info = self.parse_proxy_info(proxy_info)
                if parsed_proxy_info is None:
                    self.log(
                        f"{red}Check proxy format: {white}http://user:pass@ip:port"
                    )
                    break
                ip_adress = parsed_proxy_info["ip"]
                self.log(f"{green}Input IP Address: {white}{ip_adress}")

                ip = self.check_ip(proxy_info=proxy_info)
                self.log(f"{green}Actual IP Address: {white}{ip}")

                # Get user info
                try:
                    auth_user = self.auth_user(data=data, proxy_info=proxy_info).json()
                    auth_data = auth_user["access_token"]

                    while True:
                        user_info = self.farming(
                            auth_data=auth_data, proxy_info=proxy_info
                        ).json()

                        user_id = user_info["telegram_id"]
                        balance = user_info["balance"]
                        farming_status = user_info["session"]["status"]
                        self.log(f"{green}ID: {white}{user_id}")
                        self.log(f"{green}Balance: {white}{balance:,}")
                        if farming_status == "await":
                            self.log(f"{yellow}Farming not started yet")
                            start_farming = self.start_farming(
                                auth_data=auth_data, proxy_info=proxy_info
                            )
                            if start_farming.status_code == 200:
                                self.log(f"{green}Start farming successful")
                                break
                            else:
                                self.log(f"{red}Start farming failed")
                                break

                        check_in = self.check_in(
                            auth_data=auth_data, proxy_info=proxy_info
                        )
                        if check_in.status_code == 200:
                            self.log(f"{green}Check in successful")
                        else:
                            self.log(f"{yellow}Checked in already")

                        tap = random.randint(1000000, 2000000)
                        finish_farming = self.finish_farming(
                            auth_data=auth_data, tap=tap, proxy_info=proxy_info
                        )
                        if finish_farming.status_code == 200:
                            self.log(f"{green}Finish farming successful")
                        else:
                            self.log(f"{yellow}In farming status, claim later")
                            break

                    try:
                        tasks = self.check_task(
                            auth_data=auth_data, proxy_info=proxy_info
                        ).json()
                        for task in tasks:
                            task_id = task["id"]
                            task_name = task["name"]
                            task_status = task["status"]
                            if task_status == "possible":
                                complete_task = self.complete_task(
                                    auth_data=auth_data,
                                    task_id=task_id,
                                    proxy_info=proxy_info,
                                )
                                status = complete_task.json()["task"]["status"]
                                if (
                                    complete_task.status_code == 200
                                    and status != "possible"
                                ):
                                    self.log(f"{white}{task_name}: {green}Completed")
                                else:
                                    self.log(f"{white}{task_name}: {red}Incompleted")
                            else:
                                pass
                    except Exception as e:
                        self.log(f"{red}Check task error!!!")

                    try:
                        ref_claim = self.ref_claim(
                            auth_data=auth_data, proxy_info=proxy_info
                        ).json()
                        balance = ref_claim["balance"]
                        claimed_amount = int(ref_claim["sum"])
                        if claimed_amount > 0:
                            self.log(
                                f"{green}Claimed from ref: {white}{claimed_amount:,}"
                            )
                            self.log(f"{green}Current balance: {white}{balance:,}")
                        else:
                            self.log(f"{yellow}No point from ref")
                    except Exception as e:
                        self.log(f"{red}Claim from ref error!!!")
                except Exception as e:
                    self.log(f"{red}Get user info error!!!")

            print()
            wait_time = 60 * 60
            self.log(f"{yellow}Wait for {int(wait_time/60)} minutes!")
            time.sleep(wait_time)


if __name__ == "__main__":
    try:
        bump = BUMP()
        bump.main()
    except KeyboardInterrupt:
        sys.exit()
