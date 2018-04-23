'''

'''



import urllib.request
import re
import os
from bs4 import BeautifulSoup as BFS


class GET_Pic_Fuc():
    def __init__(self):
        self.num_of_page = []  # 存储soup处理的html的页面数
        self.soup_list = []  # 存储未处理的soup
        self.list_of_src_for_pic = {}  # 存储从soup_for_pic 查找出来的pic的src
        self.listToDelete = []  # 剩余需要下载的数据
        self.list_num_own = []  # 本地所持有的数据号码
        self.soup_for_pic = None  # 生成img标签的soup
        self.list_of_data_compare_with_listToDelete = []  # 对比剩余数据未下载的数据得到本次需要下载的数据
        self.listOf_OriginalData = []

    # 生成soup
    def soup_make_fuc(self, url, page_args, user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36 115Browser/8.4.0'):

        # 生成url
        def url_make_fuc(url, page_args):
            return url + page_args

        # 设置基本属性, url ,user_agent 之类的头部信息
        url = url_make_fuc(url, page_args)
        self.soup_list = []

        # 生成request请求
        headers = {'user-agent': user_agent}
        request = urllib.request.Request(url, headers=headers)

        # 传出request,接收response
        try:
            response = urllib.request.urlopen(request, timeout=10)
            # 用beautifulsoup处理,这里在read()之后进行decode处理可以加快运行速度,不知道为什么....
            html_page = response.read().decode(encoding='utf-8', errors='ignore')
            soup = BFS(html_page, "lxml")
            # 以下为展示soup整理格式的代码
            # soup_prettify = soup.prettify()
            return soup
        except urllib.error.HTTPError as e:
            print(e.code)
        except urllib.error.URLError as e:
            print(e.reason)


    # 生成soup集的方法
    def soups_list_make_fuc(self, num_of_th_last_page, soup_make_fuc_a):
        soup_list_new = []
        for page_args in list(range(1, num_of_th_last_page + 1)):
            soup = self.soup_make_fuc('https://sukebei.nyaa.si/?f=0&c=0_0&q=259luxu&p=', str(page_args),
                                      user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36 115Browser/8.4.0')
            soup_list_new.append(soup)
        # 存储起来
        self.soup_list = soup_list_new

    # 截取数据段
    def get_key_of_data(self, str_a, key_str, keep_num_after_key):
        if key_str in str_a:
            return str_a.split(key_str)[1][1:keep_num_after_key]

    # 列出所需要的data并且加入到list:listOf_OriginalData中
    def listName_of(self, dir):
        self.listOf_OriginalData = []
        for a, b, files in os.walk(dir):
            for name in files:
                self.listOf_OriginalData.append(str(name).lower())

    # 生成一个list用来存剩余需要下载的数据编号
    def get_list_of_data_to_delete(self, data_list, str_of_get_key_of_data, num_of_key_of_data):
        self.listToDelete = []
        self.list_num_own = []
        num_own = None
        count_error = 0
        for data in data_list:
            num_own_saved = str(num_own)
            num_own = self.get_key_of_data(
                data, str_of_get_key_of_data, num_of_key_of_data)

            try:
                num_own = int(num_own)
            except:
                count_error = count_error + 1
                print('在list_num_own的位置:', num_own_saved,
                      '之后', '出错名为', str(num_own))
            self.list_num_own.append(num_own)
        print('累计出错:  ', count_error)
        self.listToDelete = list(
            set(range(1, 1000)).difference(set(self.list_num_own)))

    # 对比本地所有数据集和网络数据集,取得差集,获取图片src的list
    def findAndCompile_get_img_src_list(self, args_forSearch='(?i)259LUXU.+\.jpg'):

        # 查找alt标签
        soup_for_pic_next = self.soup_for_pic.find_next(
            alt=re.compile(args_forSearch))
        self.soup_for_pic = soup_for_pic_next

        # 如果没找到数据
        if str(soup_for_pic_next) == 'None':
            print('No More In This Page')
            return None

        # 若找到数据进行处理
        else:
            # 比对数据库文件,查看是否存在这个文件,存在则跳过,不存在则获取src并且存到list_of_src_for_pic
            Data_to_compare = self.get_key_of_data(
                str(soup_for_pic_next.get('alt')).lower(), '259luxu', 4)
            Data_to_compare_saved = Data_to_compare
            try:
                Data_to_compare = int(Data_to_compare)
                # print(Data_to_compare)
            except:
                print('网页问题文件名:', Data_to_compare_saved)
            if Data_to_compare in self.listToDelete:
                self.list_of_data_compare_with_listToDelete.append(
                    Data_to_compare)
                self.listToDelete.remove(Data_to_compare)
                get_src = str((soup_for_pic_next.get('src')))
                # 引入存储图片src的list
                self.list_of_src_for_pic[Data_to_compare] = get_src

            return self.findAndCompile_get_img_src_list(args_forSearch)

    # 获取list_of_src_for_pic中的src ,下载并保存图片到本地
    def downloadpic(self):
        for name_of_img, img_src in self.list_of_src_for_pic.items():
            urllib.request.urlretrieve(img_src, '/Volumes/innov8/FKT/259luxu大制作/259LUXU封面/' + '%s.jpg' % ('259LUXU-'+str(name_of_img)))


if __name__ == '__main__':
    # 生成实例
    run_server = GET_Pic_Fuc()
    soup_list_new = run_server.soup_list
    # 设置基本属性, url ,user_agent 之类的头部信息
    # 生成soup集: soup_list_new
    for page_args in list(range(1, 69)):
        soup = run_server.soup_make_fuc('http://www.ziyuandaigou.com/luxu/page/', str(page_args),
                                        user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36 115Browser/8.4.0')
        soup_list_new.append(soup)
    print('搜寻的页面数量:', len(soup_list_new))

    # 以下为调试使用
    # with open('soup_txt.txt', 'w') as soup_file:
    #     for soup_a in soup_list_new:
    #         soup_file.writelines(str(soup_a) + '\n')

    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')

    # 生成listOf_OriginalData
    run_server.listName_of('/Volumes/innov8/FKT/259luxu大制作/259LUXU封面')
    # print(run_server.listOf_OriginalData)

    # 生成lsit_num_own(所拥有的数据号); 生成listToDelete(不曾拥有的数据号)
    run_server.get_list_of_data_to_delete(
        run_server.listOf_OriginalData, '259luxu', 4)
    print('以上为本地出错点')
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')

    # 处理soup并且搜寻关键字
    soup_count_page = 0  # 计算soup 网页页数
    for soup in soup_list_new:
        soup_count_page = soup_count_page + 1
        # 生成img标签的soup
        run_server.soup_for_pic = soup.img
        # 传入比对信息获取需要的src
        run_server.findAndCompile_get_img_src_list('(?i)259LUXU.+')
        print('页数 : 第', soup_count_page, '页')

    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')

    # 打印展示本次需要下载的数据
    tag_of_data_need_to_download = run_server.list_of_data_compare_with_listToDelete
    print('经过比对需要下载的数据为:', tag_of_data_need_to_download)

    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    # print(run_server.list_of_src_for_pic)

    # 将magnet写入到magnet_txt.txt文件中
    with open('src_txt.txt', 'w') as src_file:
        for num, src in run_server.list_of_src_for_pic.items():
            src_file.writelines(str(num) + ':  ' + str(src) + '\n')

    # #下载src
    run_server.downloadpic()

    #打印结束提示语
    print('all right')
