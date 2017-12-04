from scrapy.selector import HtmlXPathSelector as hpath
import requests
import shutil
import os
class Torrents(object):
    headers = {
        'Host': 'bt.byr.cn',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Cookie': 'Hm_lvt_9ea605df687f067779bde17347db8645=1490784554,1490786320,1491579022; c_secure_ssl=bm9wZQ%3D%3D; _ga=GA1.2.590237241.1493463694; byrbta153=1; byrbta1=1; byrbta=1; byrbta2=1; byrbta3=1; byrbta4=1; _gid=GA1.2.1557381386.1512106040; c_secure_uid=MjM3Nzk3; c_secure_pass=1ee25476ea4842f1ab103364d59ae905; c_secure_tracker_ssl=bm9wZQ%3D%3D; c_secure_login=bm9wZQ%3D%3D; _gat=1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'}

    def __init__(self):
        self.links=self.get_torrents_link()
        self.index=0
        self.max_index=len(self.links)

    def get_torrents_link(self):
        open_page='http://bt.byr.cn/torrents.php?spstate=2&sort=8&type=desc'
        download_page='http://bt.byr.cn/'
        page = requests.get(url=open_page,headers=self.headers)
        if page.status_code!=200:
            raise Exception("link error!")
        page = hpath(page)
        ts = page.xpath("//*[@class='download']/..//@href").extract()
        ts = map(lambda x:download_page+x,ts)

        return ts

    def download_torrents(self,link):
        r = requests.get(link, headers=self.headers, stream=True)
        if r.status_code == 200:
            path=os.path.join('torrent_file_temp',link.split('=')[1]+'.torrent')
            with open(path, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
            return os.path.abspath(path)
        return None

    def __iter__(self):
        return self

    def __call__(self, *args, **kwargs):
        return self.__next__()

    def __next__(self):
        if self.index<self.max_index:
            path=self.download_torrents(self.links[self.index])
            self.index+=1
            return path
        else:
            raise StopIteration


if __name__ =='__main__':
    t = Torrents()
    while(True):
        try:
            t()
        except StopIteration:
            break