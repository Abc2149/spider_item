import requests, re, json, os
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from requests.exceptions import  RequestException
import demjson
from hashlib import md5
from config import *
import pymongo
from multiprocessing import Pool

# client = pymongo.MongoClient(MONGO_URL)
# db = client[MONGO_DB]

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36',
    }

def get_page_index(offset,keyword):
    '''
    获取主页的HTML函数
    :param offset: 页面动态加载的关键参数
    :param keyword: 查询的关键字
    :return: 主页HTML
    '''
    # 客户端发送的请求数据
    data={
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': 20,
        'cur_tab': 3,
        'from': 'gallery',
    }
    # 通过urllib.urlencode 构建url链接
    url = 'https://www.toutiao.com/search_content/?'+urlencode(data)
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:      # 请求成功的状态码
            return response.text             # 返回HTML内容
        return None
    except RequestException:
        print('请求主页信息失败')
        return None

def parse_page_index(html):
    '''
    解析主页内容中的详情页URL
    :param html: 主页HTML
    :return: 详情页url链接
    '''
    # json格式的字符串数据转化为python字典列表的形式
    # 提取详情页的URL
    data = json.loads(html)     # 将json内容转化为python格式的字典形式
    if data and 'data' in data.keys():     # 判断data字段是否在对象中
        for item in data.get('data'):      # 获取data字段的value
            yield item.get('article_url')  # 返回详情页的url链接

def get_page_detail(url):
    '''
    获取详情页的内容函数
    :param url: 详情页的url链接
    :return: 详情页内容
    '''
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求详情页失败')
        return None

def parse_page_detail(html,url):
    '''
    解析详情页中的图片标题和url链接
    :param html: 详情页内容
    :param url: 详情页url
    :return: 标题 详情页url 图片url
    '''
    # 用bs4库HTML页面，提取标题和图片链接
    soup = BeautifulSoup(html,'lxml')
    # 提取标题
    title = soup.select('title')[0].get_text()
    # 利用正则表达式提取图片对象
    image_pattern = re.compile('gallery: JSON.parse(.*?)"]}"',re.S)
    result = re.search(image_pattern,html)

    data = eval(json.loads(result.group(1)[1:]+'"]}"'))
    if data and 'sub_images' in data.keys():
        sub_images = data.get('sub_images')
        images = [item.get('url') for item in sub_images]
        images = [images.replace('\\','') for images in images]
        for images in images:
            download_image(images)
        # print(images)
        return {
            'title':title,
            'url': url,
            'images':images,
        }


# def save_to_mongo(result):
#     if db[MONGO_TABLE].insert(result):
#         print("存储到MongoDB成功")
#         return True
#     return False

def download_image(url):
    '''
    下载图片
    :param url: 图片URL
    :return: 图片二进制内容
    '''
    print('正在下载',url)
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            save_images(response.content)
        return None
    except RequestException:
        print('下载图片失败')
        return None

def save_images(content):
    '''
    保存图片到文件夹
    :param content: 图片二进制内容
    :return: 无
    '''
    filname = 'D:/Desktop/python爬虫/Ajax_jinritoutiao/images/'+str(md5(content).hexdigest())+'.jpg'
    with open(filname,'wb') as f:
        f.write(content)

def main(offset):
    '''
    主函数
    :param offset: 页面动态加载的关键参数
    :return: 无
    '''
    html = get_page_index(offset,'街拍')   # 主页HTML
    for url in parse_page_index(html):   # 详情页面URL
        html = get_page_detail(url)        # 详情页HTML
        result = parse_page_detail(html,url)    # 解析详情页HTML
        # save_to_mongo(result) # 保存到MangoDB


if __name__ == '__main__':
        pool = Pool()
        pool.map(main, [i*20 for i in range(0,10)])