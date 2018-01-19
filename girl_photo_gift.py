import requests
import re
import os
from multiprocessing.dummy import  Pool
from random import randint

class photo():
    '''_爬虫_ ，没做容错处理 乱输入会直接报错
    多线程+正则+requests库的使用+类的调用+读写文件
    '''

    def __init__(self):
        self.url_origin = 'https://www.nvshens.com/gallery/'
        ##维持一个session
        self.s=requests.session()
        ##类型列表
        self.li_specy= self.species()
        ##你选的类型
        self.your_answer, self.deep = self.select()
        ##选的次页数
        self.a = int(input('请输入图集页数,图集一页有五张图片，图集页数最好在8以下：'))
        ##拼接 你所选的文件总数
        self.li_spell_you_spell=self.apell_you_select()
        ##再次拼接 你所选的文件单一数
        self.li_photo_web=self.apell_you_select_again()

    ##抓取类型:
    def species(self):
        response=self.s.get(self.url_origin)
        response.encoding=response.apparent_encoding
        text=response.text
        li_specy=re.findall(r"<a href='/gallery/(.*?)/'>",text,re.S)
        return li_specy

    ##给出 你的选择，看个人兴趣,(I select jiaoxiao)
    def select(self):
        print('可以下载各种类型的美女图片,速度挺快的')
        print('类型简写:谁叫这网站作者取这奇葩名字')
        for i in range(len(self.li_specy)):
            print(self.li_specy[i],' ,',end='')
            if i %12==0:
                print()
        print()
        print()
        your_answer=input('你选的类型:')
        print()
        print()
        deep=input('请输入页数,一页30个图集：')
        return your_answer,deep

    ##拼接 你所选的文件总数
    def apell_you_select(self):

        url_file=self.url_origin+self.your_answer
        ##输入 1 为空
        url_files=[(url_file+r'/'+str(i)+'.html') for i in range(2,int(self.deep)+1)]
        url_files.append(url_file)
        return url_files

    ##再次拼接 你所选的文件单一数
    def apell_you_select_again(self):
        url_one='https://www.nvshens.com'
        li_photo_web=[]
        for url in self.li_spell_you_spell:
            response = self.s.get(url)
            response.encoding = response.apparent_encoding
            text = response.text
            li=re.findall(r"<a class='galleryli_link' href='(.*?)' >",text)
            li_photo_web.extend(li)
        li_photo_web = list(map(lambda x: url_one + x, li_photo_web))
        # print(li_photo_web)
        return li_photo_web

    # 创建文件夹 得图片地址,路径
    def download_creat_path(self):
        li=[]
        for url in self.li_photo_web:
            response = self.s.get(url)
            response.encoding = response.apparent_encoding
            text = response.text
            li.extend(re.findall(r'<title>(.*?)</title>',text))
        paths = list(map(lambda x: r'photo/' + x, li))

        li_download = self.li_photo_web

        for path,url_1 in zip(paths,li_download):
            li_photos = []

            if os.path.exists(path):
                pass
            else:
                os.makedirs(path)
            ##看你需要的页数
                for page in range(1, self.a+1):
                    url_1=url_1+str(page)+'.html'
                    # print(url)
                    response = self.s.get(url_1)
                    response.encoding = response.apparent_encoding
                    text_photo = response.text
                    li_photos.extend(re.findall(r"<img src='(.*?)'",text_photo))
                self.main(li_photos,path)
        print('一共下载了{}个图集，{}张图片'.format(int(self.deep)*30,int(self.deep)*self.a*5*30))


    ##下载
    def  download(self,url,path):
        r=self.s.get(url)
        content_photo=r.content
        a=path+r'/'+'%d'%randint(-100,300000000000)+r'.jpg'
        print(a)
        with open(a,'wb') as f:
            f.write(content_photo)

    ##多线程
    def main(self,li_url,path):
        pool = Pool(4)
        for url in  li_url:
            pool.apply_async(self.download, args=(url,path))
        pool.close()
        pool.join()


if __name__ == '__main__':
    a=photo()
    a.download_creat_path()
    input('程序结束,按任意键退出')