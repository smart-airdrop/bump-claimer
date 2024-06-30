import os
import sys
import time
import requests
from colorama import *
from datetime import datetime
import random
import brotli

# Color setup
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


# Clear the terminal
def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")


class MMBump:
    def __init__(self):
        self.auth_url = "https://api.mmbump.pro/v1/auth"
        self.common_headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://mmbump.pro",
            "Referer": "https://mmbump.pro/",
            "Sec-Ch-Ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            "Sec-Ch-Ua-Mobile": "?1",
            "Sec-Ch-Ua-Platform": '"Android"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
        }
        self.user_agents = [
            "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            # add more if needed
        ]
        self.line = white + "~" * 50
        self.telegram_ids = self.load_telegram_ids()

    def load_telegram_ids(self):
        with open(data_file, "r", encoding="utf8") as f:
            return f.read().strip().split("\n")

    def log(self, msg):
        now = datetime.now().isoformat(" ").split(".")[0]
        print(f"{black}[{now}] {reset}{msg}")

    def http_request(self, url, headers, data=None):
        while True:
            try:
                if data is None:
                    return requests.get(url, headers=headers)
                return requests.post(url, headers=headers, data=data)
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
                self.log(f"{red}Connection error / Connection timeout !")
                time.sleep(1)
                continue

    def check_farming_status(self, farming_data, farming_headers):
        current_time = int(time.time())
        if (
                farming_data["session"]["status"] == "inProgress"
                and current_time > farming_data["session"]["moon_time"]
        ):
            self.complete_farming(farming_headers)
            self.log(f"{green}Rechecking balance...")
            self.recheck_balance(farming_headers)
        else:
            self.log(f"{yellow}Farming in progress")

    def complete_farming(self, farming_headers):
        try:
            rd_tap_count = random.randint(50000, 150000)
            finish_url = "https://api.mmbump.pro/v1/farming/finish"
            finish_payload = {"tapCount": rd_tap_count}
            finish_response = self.http_request(
                finish_url, farming_headers, finish_payload
            )

            if finish_response.status_code == 200:
                self.log(f"{green}Farming completed")
                self.start_farming(farming_headers)
            else:
                self.log(f"{red}Error completing farming: {finish_response.json()}")
        except requests.RequestException as error:
            self.log(f"{red}Error completing farming: {str(error)}")
            if error.response:
                self.log(f"{red}Response data: {error.response.json()}")

    def start_farming(self, farming_headers):
        farming_start_url = "https://api.mmbump.pro/v1/farming/start"
        farming_start_payload = {"status": "inProgress"}
        start_response = self.http_request(
            farming_start_url, farming_headers, farming_start_payload
        )

        if start_response.status_code == 200:
            self.log(f"{green}Farming started...")
        else:
            self.log(f"{red}Error starting farming: {start_response.json()}")

    def handle_daily_checkin(self, farming_data, farming_headers):
        current_time = int(time.time())
        if (
                farming_data["day_grant_first"] is None
                or (current_time - farming_data["day_grant_first"]) >= 86400
        ):
            grant_day_claim_url = "https://api.mmbump.pro/v1/grant-day/claim"
            self.http_request(grant_day_claim_url, farming_headers, data={})
            self.log(f"{green}Daily check-in completed")
        else:
            self.log(f"{yellow}Daily check-in already done")

    def handle_farming(self, telegram_id, user_agent):
        auth_payload = f"telegram_id={telegram_id}"
        headers = {**self.common_headers, "User-Agent": user_agent}

        try:
            auth_response = self.http_request(
                self.auth_url, headers, data=auth_payload
            )
            if auth_response.status_code == 200:
                hash_token = self.extract_hash(auth_response)
                farming_headers = {**headers, "Authorization": hash_token}
                farming_data = self.get_farming_data(farming_headers)

                if farming_data:
                    self.log(f'{green}ID: {white}{farming_data["telegram_id"]}')
                    self.log(f'{green}Balance: {white}{farming_data["balance"]:,}')
                    self.handle_daily_checkin(farming_data, farming_headers)

                    if farming_data["session"]["status"] == "await":
                        self.start_farming(farming_headers)
                    else:
                        self.check_farming_status(farming_data, farming_headers)
                else:
                    self.log(
                        f"{red}Unable to get valid farming data after multiple attempts"
                    )
            else:
                raise Exception("Unable to authenticate")
        except requests.RequestException as error:
            self.log(f"{red}Error occurred: {error}")

    def extract_hash(self, auth_response):
        try:
            hash_token = (
                brotli.decompress(auth_response.content).decode("utf-8").json()["hash"]
            )
        except:
            hash_token = auth_response.json()["hash"]

        return hash_token

    def get_farming_data(self, farming_headers):
        farming_url = "https://api.mmbump.pro/v1/farming"
        farming_data = None
        attempts = 0
        max_attempts = 5

        while attempts < max_attempts:
            farming_response = self.http_request(farming_url, farming_headers)
            if farming_response.status_code == 200:
                farming_data = farming_response.json()
                if "telegram_id" in farming_data and "balance" in farming_data:
                    break
            attempts += 1
            self.log(f"{yellow}Retrying attempt {attempts} to get farming data...")

        return farming_data

    def recheck_balance(self, farming_headers):
        farming_data = self.get_farming_data(farming_headers)
        if farming_data:
            self.log(f'{green}Rechecked Balance: {white}{farming_data["balance"]:,}')
        else:
            self.log(f"{red}Unable to recheck balance after farming completion")

    def countdown(self, t):
        while t:
            hours, remainder = divmod(t, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_left = (
                f"{str(hours).zfill(2)}:{str(minutes).zfill(2)}:{str(seconds).zfill(2)}"
            )
            print(f"{white}Time left: {time_left} ", flush=True, end="\r")
            t -= 1
            time.sleep(1)
        print("                          ", flush=True, end="\r")

    def main(self):
        clear_terminal()
        self.print_banner()
        if len(self.telegram_ids) <= 0:
            self.log(f"{red}Add data account in data.txt first !")
            sys.exit()
        self.log(f"{blue}Number of accounts: {white}{len(self.telegram_ids)}")
        if len(self.telegram_ids) > len(self.user_agents):
            self.log(f"{red}Not enough unique user-agents for all accounts")
            sys.exit()
        while True:
            for no, telegram_id in enumerate(self.telegram_ids):
                user_agent = self.user_agents[no % len(self.user_agents)]
                print(self.line)
                self.log(
                    f"{blue}Account number: {white}{no + 1}/{len(self.telegram_ids)} - {user_agent}"
                )
                self.handle_farming(telegram_id.strip(), user_agent)

            print(self.line)
            wait_time = 60 * 60
            self.log(f"{yellow}Wait for {int(wait_time / 60)} minutes")
            self.countdown(wait_time)

    def print_banner(self):
        banner = f"""
        {blue}Smart Airdrop {white}Bump Auto Claimer
        t.me/smartairdrop2120
        """
        print(banner)


if __name__ == "__main__":
    try:
        mmbump = MMBump()
        mmbump.main()
    except KeyboardInterrupt:
        sys.exit()
