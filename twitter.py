import asyncio
import json
import logging
import random
from time import sleep

import requests
from config import proxy, bot, tg_user_id, flower

import uuid

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


tweet_latest = {}
def get_user_id(screen_name,csrf,cookie):
    url = f'https://x.com/i/api/graphql/laYnJPCAcVo0o6pzcnlVxQ/UserByScreenName?variables=%7B%22screen_name%22%3A%22{screen_name}%22%7D&features=%7B%22hidden_profile_subscriptions_enabled%22%3Atrue%2C%22rweb_tipjar_consumption_enabled%22%3Atrue%2C%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22subscriptions_verification_info_is_identity_verified_enabled%22%3Atrue%2C%22subscriptions_verification_info_verified_since_enabled%22%3Atrue%2C%22highlights_tweets_tab_ui_enabled%22%3Atrue%2C%22responsive_web_twitter_article_notes_tab_enabled%22%3Atrue%2C%22subscriptions_feature_can_gift_premium%22%3Atrue%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%7D&fieldToggles=%7B%22withAuxiliaryUserLabels%22%3Afalse%7D'
    defaulf_headers = {
        "authority": "x.com",
        'accept-encoding': '',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'priority': 'u=1, i',
        'x-twitter-auth-type': 'OAuth2Session',
        'referer': 'https://x.com/elonmusk',
        'sec-ch-ua': '"Chromium";v="130", "Microsoft Edge";v="130", "Not?A_Brand";v="99"',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0',
        "x-twitter-active-user": "yes",
        "x-twitter-client-language": "zh-CN",
        "authorization": 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
        'content-type': 'application/json',

        'x-csrf-token': csrf,
        'x-client-transaction-id': 'YbQzqKVavmiebL5BTbsPCs+pGu5VpPRfBqLevdF4IEGtHGDHWUZECyGokbkayaT6/QFfh2MUnir2KNATcoi+AqMVL+zDYg',
        'x-client-uuid': '8f7d201e-f5ec-48f0-98ad-090e046ec194',
        'cookie': cookie

    }
    try:
        res = requests.get(url, headers=defaulf_headers, proxies=proxy)
        res = res.json()
        userId = res["data"]["user"]["result"]["rest_id"]
        return userId
    except Exception as e:
        logging.info(e)


def monitor(userId,csrf,cookie):
        global tweet_latest
        url = f'https://x.com/i/api/graphql/F_gCJRQooCZ0T74rGl4q9Q/UserTweets?variables=%7B%22userId%22%3A%22{userId}%22%2C%22count%22%3A20%2C%22includePromotedContent%22%3Atrue%2C%22withQuickPromoteEligibilityTweetFields%22%3Atrue%2C%22withVoice%22%3Atrue%2C%22withV2Timeline%22%3Atrue%7D&features=%7B%22responsive_web_live_screen_enabled%22%3Afalse%2C%22rweb_tipjar_consumption_enabled%22%3Atrue%2C%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22communities_web_enable_tweet_community_results_fetch%22%3Atrue%2C%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Atrue%2C%22articles_preview_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Atrue%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22creator_subscriptions_quote_tweet_preview_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22rweb_video_timestamps_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D&fieldToggles=%7B%22withArticlePlainText%22%3Afalse%7D'
        # print(url)
        defaulf_headers = {
            "authority": "x.com",
            'accept-encoding': '',
            'accept':'*/*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'priority':'u=1, i',
            'x-twitter-auth-type': 'OAuth2Session',
            'referer':'https://x.com/elonmusk',
            'sec-ch-ua':'"Chromium";v="130", "Microsoft Edge";v="130", "Not?A_Brand";v="99"',
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0',
            "x-twitter-active-user": "yes",
            "x-twitter-client-language": "zh-CN",
            "authorization": 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
            'content-type': 'application/json',
            'x-csrf-token':csrf,
            'x-client-transaction-id': 'YbQzqKVavmiebL5BTbsPCs+pGu5VpPRfBqLevdF4IEGtHGDHWUZECyGokbkayaT6/QFfh2MUnir2KNATcoi+AqMVL+zDYg',
            'x-client-uuid': '8f7d201e-f5ec-48f0-98ad-090e046ec194',
            'cookie': cookie

        }


        try:
            res = requests.get(url,headers = defaulf_headers,proxies = proxy)
            res = res.json()


            tweet_type = res["data"]["user"]["result"]["timeline_v2"]["timeline"]["instructions"][1]["type"]
            user_name = ''
            tweet_id = ''
            tweet_created_at = ''
            tweet_text = ''
            tweet_favorite_count = ''
            tweet_retweet_count = ''
            if tweet_type == "TimelinePinEntry":  #有置顶推文
                #获取简介描述
                res= res["data"]["user"]["result"]["timeline_v2"]["timeline"]["instructions"][2]["entries"][0]["content"]["itemContent"]["tweet_results"]["result"]
                user_id = res["core"]["user_results"]["result"]["rest_id"]
                user_name = res["core"]["user_results"]["result"]["legacy"]["name"]  # 名称
                user_screen_name = res["core"]["user_results"]["result"]["legacy"]["screen_name"]  # @后的名称
                user_followers_count = res["core"]["user_results"]["result"]["legacy"]["followers_count"]  # 粉丝数
                user_description = res["core"]["user_results"]["result"]["legacy"]["description"]  # 个人描述

                # 提取最新推文基本信息
                tweet_id = res['rest_id']
                tweet_text = res["legacy"]["full_text"]
                tweet_created_at = res["legacy"]["created_at"]
                tweet_favorite_count = res["legacy"]["favorite_count"]
                tweet_retweet_count = res["legacy"]["retweet_count"]
            if tweet_type == "TimelineAddEntries":  #无置顶推文
                res = res["data"]["user"]["result"]["timeline_v2"]["timeline"]["instructions"][1]["entries"][0]["content"]["itemContent"]["tweet_results"]["result"]

                # 获取简介描述
                user_id = res["core"]["user_results"]["result"]["rest_id"]

                user_name = res["core"]["user_results"]["result"]["legacy"]["name"]  # 名称
                user_screen_name = res["core"]["user_results"]["result"]["legacy"]["screen_name"]  # @后的名称
                user_followers_count = res["core"]["user_results"]["result"]["legacy"]["followers_count"]  # 粉丝数
                user_description = res["core"]["user_results"]["result"]["legacy"]["description"]  # 个人描述

                # 提取最新推文基本信息
                tweet_id = res['rest_id']
                tweet_text = res["legacy"]["full_text"]
                tweet_created_at = res["legacy"]["created_at"]
                tweet_favorite_count = res["legacy"]["favorite_count"]
                tweet_retweet_count = res["legacy"]["retweet_count"]

            if tweet_id !='' and tweet_id != tweet_latest.get(user_screen_name):
                message = f'{user_name}新发送推文:{tweet_text}'
                bot.send_message(tg_user_id,message)
                logging.info(message)
                tweet_latest.update({user_screen_name: tweet_id})
        except Exception as e:
            logging.info(e)



def write_line(file_path, line):
    with open(file_path, 'a') as file:
        file.write(line+'\n')

def main():


    tokens = []


    logging.info('开始进行')
    lines = open('tw.txt','r').readlines()
    for line in lines:
        token_info = []
        token_info.append(line.split('----')[0])
        token_info.append(line.split('----')[1])
        tokens.append(token_info)

    userIds = []

    for i in flower:
        use_token = random.choice(tokens)

        token = use_token[0]
        cookie = use_token[1]
        userIds.append(get_user_id(i,token,cookie))

    while True:

        for i in range(0,len(userIds)):
            use_token = random.choice(tokens)

            csrf = use_token[0]
            cookie = use_token[1]

            monitor(userIds[i],csrf,cookie)

        sleep(10)



if __name__ == '__main__':
    # _file_name = input('账号文件(eth----privateKey----auth_token一行一个，放txt，拖入): ').strip()
    _file_name = ''
    main()