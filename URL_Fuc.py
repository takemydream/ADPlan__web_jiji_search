# 此文件存储了用于url处理的函数

import urllib.request
import urllib.parse
import urllib.error
import urllib.response
import ADTPlan_Args as ADTPA
from bs4 import BeautifulSoup
# from bs4.diagnose import diagnose
# from bs4 import NavigableString

import logging
logger = logging.getLogger(__name__)


# '生成url'
def url_make_fuc(url, page_args, string_At_The_End):

    mixStringUp =  url + page_args
    mixStringUp = mixStringUp + string_At_The_End
    logger.debug(mixStringUp)
    return mixStringUp

#TODO 这里若是查找逻辑变了就需要修改
'''
# 传入的参数: url, page_args, string_At_The_End, user_agent
# 传出:      soup
'''
# 生成soup
def soup_make_fuc(url, page_args, string_At_The_End, user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:58.0) Gecko/20100101 Firefox/58.0' ):
    # 设置基本属性, url ,user_agent 之类的头部信息
    ADTPA.soup_list = []
    url = url_make_fuc(url, page_args, string_At_The_End)
    # 这里有些需要验证的属性需要设置添加

    # 生成request请求,上面需要添加的属性也需要添加到头部文件
    # headers = {'user-agent': user_agent, 'Referer': referer}
    headers = {'user-agent': user_agent}
    request = urllib.request.Request(url, headers=headers)

    # 传出request,接收response
    try:
        response = urllib.request.urlopen(request, timeout=10)
        # 用beautifulsoup处理,这里在read()之后进行decode处理可以加快运行速度,不知道为什么....
        html_page = response.read().decode(encoding='utf-8', errors='ignore')
        soup = BeautifulSoup(html_page, "lxml")
        # 去掉以下注解展示soup整理格式的代码
        # soup_prettify = soup.prettify()
        if soup != None:
            return soup
        else:
            print("soup 为空")
    except urllib.error.HTTPError as e:
        print(e.code)
    except urllib.error.URLError as e:
        print(e.reason)
    except:
        print("unknow except in URL_Fuc.py .soup_make_fuc, we need to fix it ")



'''
# 传入的参数: soup
# 输出     : none
# 单独保存每一个soup.,保存成一个txt文件
'''
# 生成一堆txt 文件,用来存储各个soup;
def soup_write_into_txt(soup, page_arg):
    str_txt_name = "第" + str(page_arg) + "页的soup.txt"
    with open("soup_saved_file/" + str_txt_name, "w") as soup_file:
        soup_file.writelines(str(page_arg) + "\n" + "这是第" + str(page_arg) + "页" + "\n" + str(soup))
