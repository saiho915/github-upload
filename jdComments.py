import requests
from urllib.parse import urlencode
from requests.exceptions import ConnectionError
import re
import json
import time
from config import *
import pymongo

client = pymongo.MongoClient(MONGO_URL, connect = False)
db = client[MONGO_DB]

def get_responseText(url): # 获取响应代码
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    }
    try:
        response = requests.get(url, headers = headers)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        print('Error occurred')
        return None

def get_one_page_comments(commentVersion, SKU):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'Referer': 'https://item.jd.com/{0}.html'.format(SKU)
    }
    data = {
        'callback': 'fetchJSON_comment98vv' + commentVersion,
        'productId': SKU,
        'score': 0,
        'sortType': 6, # 时间排序：6；推荐排序：5   
        'page': 20,
        'pageSize': 10,
        'isShadowSku': 0,
        'rid': 0,
        'fold': 1,
    }
    params = urlencode(data)
    base = 'https://club.jd.com/comment/skuProductPageComments.action'
    url = base + '?' + params
    try:
        response = requests.get(url, headers = headers)
        if response.status_code == 200:
            html =  response.text
    except ConnectionError:
        print('Error occurred')
    jsonData = json.loads(html[html.find('(')+1:-2]) # 将字典部分截取出来，倒数两位是符号“);”
    for comment in jsonData['comments']:
        for key, value in comment.items():
            print(key, value)
        break

def extractCommentVersion(SKU): # 提取评论版本号
    url = 'https://item.jd.com/{0}.html'.format(SKU)
    print(url)
    html = get_responseText(url)
    commentVersion_pattern = re.compile('commentVersion:\'(.*?)\',.*?specialAttrs', re.S)
    result = re.search(commentVersion_pattern, html)
    if result:
        print(result.group(1))
        return result.group(1)

def main(SKU):
    commentVersion = str(extractCommentVersion(SKU))
    time.sleep(1)
    get_one_page_comments(commentVersion, SKU)
    '''
    base = 'https://question.jd.com/question/getQuestionAnswerList.action?page=2&productId='
    url = base + SKU
    try:
        response = requests.get(url)
        if response.status_code == 200:
            html =  response.text
            print(html)
    except ConnectionError:
        print('Error occurred')
    '''

if __name__ == '__main__':
    SKU = str(10072865662)
    main(SKU)

# https://question.jd.com/question/getQuestionAnswerList.action?callback=jQuery8573795&page=2&productId=10072865662