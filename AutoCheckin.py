import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import argparse
import requests
import subprocess
import os
import sys
from requests.cookies import RequestsCookieJar
from requests.utils import dict_from_cookiejar, cookiejar_from_dict

class ChromeDriverDownloader:
    def __init__(self, version: str, platform: str):
        self._current_name = ""
        self._version = version
        self._version_str = self._version.split('.')
        self._platform = platform
        self._chrome_driver_version_list = []
        self._base_url = "https://chromedriver.storage.googleapis.com"

    def _get_latest_version(self):
        main_version = '.'.join(self._version_str[:3])
        response = requests.get(f"{self._base_url}/LATEST_RELEASE_{main_version}")
        return response.text

    def download_chromedriver(self):
        latest_version = self._get_latest_version()
        if latest_version == self._version:
            self._download(self._version)
        elif int(self._version_str[3]) > int(latest_version.split('.')[3]):
            self._download(latest_version)

    def _download(self, version):
        url = f"{self._base_url}/{version}/chromedriver_linux64.zip"
        print(f"downloading chrome driver from {url}")
        response = requests.get(url)
        file_name = "chromedriver.zip"
        with open(file_name, "wb") as f:
            f.write(response.content)
        if os.path.exists(file_name):
            print("download chrome driver successfully.")
        os.system("unzip chromedriver.zip -d chromedriver")
        os.remove(file_name)


def get_chrome_version():
    result = subprocess.run(['google-chrome', '--version'], stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    version = output.strip().split()[-1]
    print(f"google chrome version: {version}")
    return version

def parse_arguments():
    parser = argparse.ArgumentParser(description="CordCloud Checkin")
    parser.add_argument("-u", "--username", help="username", type=str,required=True)
    parser.add_argument("-p", "--password", help="password", type=str,required=True)
    parser.add_argument("-U","--url",help="cordcloud url",type=str,required=True)
    return parser.parse_args()

def start_checkin(username,password,url):
    options = uc.ChromeOptions()
    options.add_argument("--window-size=1280,1024")
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument("--excludeSwitches=enable-automation")
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = uc.Chrome(options=options,driver_executable_path = "./chromedriver/chromedriver")
    driver.implicitly_wait(10)
    try:

        driver.get(f'{url}/auth/login')

        email_input = driver.find_element(by=By.ID, value="email")
        email_input.send_keys(username)
        password_input = driver.find_element(by=By.ID, value="passwd")
        password_input.send_keys(password)
        driver.find_element(by=By.ID, value="login").click()
       
        print("Login success!")
       

        cookies = driver.get_cookies()
        print(cookies)
        c={}
        for cookie in cookies:
            cookie = dict(cookie)
            c[cookie["name"]] = cookie["value"]
        
        response = requests.post(f'{url}/user/checkin', cookies=c, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.52",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": url,
            "Referer": f"{url}/user"
        },timeout=10)

        print(response.json())
    
    except Exception as e:
        print(e)
    finally:
        driver.quit()


def download_chromedriver():
    chrome_version = get_chrome_version()
    os_type = sys.platform
    platform = "linux64"
    if os_type == "linux":
        platform = "linux64"
    elif os_type == "win32":
        platform = "win32"
    elif os_type == "darwin":
        platform = "mac64"
    downloader = ChromeDriverDownloader(chrome_version,platform)
    downloader.download_chromedriver()

def main():
    args=parse_arguments()

    username = args.username
    password = args.password
    url = args.url
    
    download_chromedriver()
    start_checkin(username,password,url)

if __name__ == '__main__':
    main()
