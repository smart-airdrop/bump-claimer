import os
import sys
import time
import requests
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
data_file = os.path.join(script_dir, "data.txt")


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

    def auth_user(self, data):
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

        response = requests.post(url=url, headers=headers, data=payload)

        return response

    def farming(self, auth_data):
        url = "https://api.mmbump.pro/v1/farming"

        headers = self.headers(auth_data=auth_data)

        response = requests.get(url=url, headers=headers)

        return response

    def start_farming(self, auth_data):
        url = "https://api.mmbump.pro/v1/farming/start"

        headers = self.headers(auth_data=auth_data)

        payload = {"status": "inProgress"}

        response = requests.post(url=url, headers=headers, data=payload)

        return response

    def finish_farming(self, auth_data, tap):
        url = "https://api.mmbump.pro/v1/farming/finish"

        headers = self.headers(auth_data=auth_data)

        payload = {"tapCount": tap}

        response = requests.post(url=url, headers=headers, data=payload)

        return response

    def check_in(self, auth_data):
        url = "https://api.mmbump.pro/v1/grant-day/claim"

        headers = self.headers(auth_data=auth_data)

        response = requests.post(url=url, headers=headers, data={})

        return response

    def log(self, msg):
        now = datetime.now().isoformat(" ").split(".")[0]
        print(f"{black}[{now}]{reset} {msg}{reset}")

    def main(self):
        while True:
            self.clear_terminal()
            print(self.banner)
            data = open(data_file, "r").read().splitlines()
            num_acc = len(data)
            self.log(self.line)
            self.log(f"{green}Numer of account: {white}{num_acc}")
            for no, data in enumerate(data):
                self.log(self.line)
                self.log(f"{green}Account number: {white}{no+1}/{num_acc}")

                # Get user info
                try:
                    auth_user = self.auth_user(data=data).json()
                    auth_data = auth_user["access_token"]

                    while True:
                        user_info = self.farming(auth_data=auth_data).json()

                        user_id = user_info["telegram_id"]
                        balance = user_info["balance"]
                        farming_status = user_info["session"]["status"]
                        self.log(f"{green}ID: {white}{user_id}")
                        self.log(f"{green}Balance: {white}{balance:,}")
                        if farming_status == "await":
                            self.log(f"{yellow}Farming not started yet")
                            start_farming = self.start_farming(auth_data=auth_data)
                            if start_farming.status_code == 200:
                                self.log(f"{green}Start farming successful")
                                break
                            else:
                                self.log(f"{red}Start farming failed")
                                break

                        check_in = self.check_in(auth_data=auth_data)
                        if check_in.status_code == 200:
                            self.log(f"{green}Check in successful")
                        else:
                            self.log(f"{yellow}Checked in already")

                        tap = random.randint(1000000, 2000000)
                        finish_farming = self.finish_farming(
                            auth_data=auth_data, tap=tap
                        )
                        if finish_farming.status_code == 200:
                            self.log(f"{green}Finish farming successful")
                        else:
                            self.log(f"{yellow}In farming status, claim later")
                            break
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
