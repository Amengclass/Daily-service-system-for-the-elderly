import requests
import re
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

def ask(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        # 将 API
        data = response.json()
        return data
    else:
        return "访问失败"


def main():
    url = 'https://whois.pconline.com.cn/ipJson.jsp?json=true'
    print(ask(url))


if __name__ == "__main__":
    main()
