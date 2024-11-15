import asyncio
import logging
import random
import sys
import httpx
from loguru import logger
from curl_cffi.requests import AsyncSession
from web3 import AsyncWeb3
from eth_account.messages import encode_defunct
import config
g_success, g_fail = 0, 0
import uuid
logger.remove()
logger.add(sys.stdout, colorize=True, format="<w>{time:HH:mm:ss:SSS}</w> | <r>{extra[fail]}</r>-<g>{extra[success]}</g> | <level>{message}</level>")
logger = logger.patch(lambda record: record["extra"].update(fail=g_fail, success=g_success))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Twitter:
    def __init__(self, auth_token):
        self.auth_token = auth_token
        bearer_token = "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"
        defaulf_headers = {
            "authority": "x.com",
            "origin": "https://x.com",
            "x-twitter-active-user": "yes",
            "x-twitter-client-language": "en",
            "authorization": bearer_token,
        }
        defaulf_cookies = {"auth_token": auth_token}
        self.Twitter = AsyncSession(headers=defaulf_headers, cookies=defaulf_cookies, timeout=120)
        self.auth_code = None
        proxy = {
            'https': 'http://127.0.0.1:8443',
            'http': 'http://127.0.0.1:8443'
        }
        self.Twitter.proxies = proxy

    async def get_ct0(self):
        try:
            logging.info('获取csrf')
            res =await self.Twitter.get('https://x.com/i/api/2/oauth2/authorize')

            self.Twitter.headers.update({'X-Csrf-Token': res.cookies.get('ct0')})

            return res.cookies

        except Exception as e:
            print(e)


def write_line(file_path, line):
    with open(file_path, 'a') as file:
        file.write(line+'\n')

async def main(file_name):

    tokens = []
    useres = []
    with open('twitter.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            token = line.strip().split('----')[4]
            user = line.strip().split('----')[0]
            tokens.append(token)
            useres.append(user)
    count = 0
    logging.info('开始进行')
    print(len(useres))
    tokens = ['69850839d417fa767f500573945b8580046bde9f']
    for i in range(0,len(useres)):

        tw = Twitter(tokens[i])
        determine = await tw.get_ct0()
        if determine != None:
            content = f'{tokens[i]}----{determine}'
            file_name = 'tw-csrf.txt'
            write_line(file_name,content)


if __name__ == '__main__':
    # _file_name = input('账号文件(eth----privateKey----auth_token一行一个，放txt，拖入): ').strip()
    _file_name = ''
    asyncio.run(main(_file_name))