from bs4 import BeautifulSoup
import urllib.request
import threading

lock = threading.Lock()    # 线程

header = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36",
    }

def getProxyList(targeturl="http://www.xicidaili.com/nn/"):
    proxyFile = open('proxy.txt', 'a', encoding='utf-8')
    counum=0
    for page in range(1, 10):
        url = targeturl + str(page)   # 页码
        req = urllib.request.Request(url, headers=header)
        html_doc = urllib.request.urlopen(req).read()

        soup = BeautifulSoup(html_doc, "lxml")
        trs = soup.find('table' ,id='ip_list').find_all('tr')
        for tr in trs[1:]:
            tds = tr.find_all('td')
            # 国家和地址
            if tds[0].find('img') is None:
                country = '未知'
                locate = '未知'
            else:
                country = tds[0].find('img')['alt'].strip()    # 国家
                locate = tds[3].text.strip()    # 服务器地址
            ip = tds[1].text.strip()            # ip
            port = tds[2].text.strip()          # 端口
            anony = tds[4].text.strip()         # 匿名
            protocol = tds[5].text.strip()      # 类型HTTP https
            speed = tds[7].find('div')['title'].strip()  # 速度
            time = tds[8].text.strip()
            # print(locate)
            proxyFile.write('%s|%s|%s|%s|%s|%s|%s|%s\n' % (country, ip, port, locate, anony, protocol, speed, time))
            counum+=1
    proxyFile.close()
    return counum


def verifyProxyList():
    '''
    验证代理的有效性
    '''
    url = 'http://www.baidu.com/'
    while True:
        lock.acquire()
        ll = inFile.readline().strip()
        lock.release()
        if len(ll) == 0:
            break
        line = ll.strip().split('|')
        protocol = line[5].lower()
        ip = line[1]
        port = line[2]
        addr=str(ip)+':'+str(port)
        try:
            req = urllib.request.ProxyHandler({protocol:addr})
            opener = urllib.request.build_opener(req,urllib.request.HTTPHandler)
            response = opener.open(url,timeout=5)
            print('请求成功状态码:',response.getcode())
            lock.acquire()
            outFile.write(addr + '\n')
            lock.release()
        except:
            print('请求失败')

def main():
    # 清空文件夹，重新存储新的内容
    with open('proxy.txt', 'w', encoding='utf-8') as f:
        f.write('')

    # 国内高匿
    proxynum = getProxyList("http://www.xicidaili.com/nn/")

    all_thread = []
    for i in range(30):
        t = threading.Thread(target=verifyProxyList)
        all_thread.append(t)
        t.start()

    for t in all_thread:
        t.join()

    inFile.close()
    outFile.close()

    print('爬取国内高匿Proxy共' + str(proxynum) + '条')
    print('验证代理的有效性结束')
    print("All Done.")

if __name__ == '__main__':

    inFile = open('proxy.txt', 'r', encoding='utf-8')
    outFile = open('verified.txt', 'w', encoding='utf-8')
    main()




