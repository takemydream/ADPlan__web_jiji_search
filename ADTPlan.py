'''
此文档为最终执行程序:仅仅用于获取磁力链, 图片需要运行GET_Pic_fuc.py
大部分数据参数存储:  在ADTPlan_Args.py
处理url和生成soup的函数存储:  URL_Fuc.py
处理soup以及生成比对本地数据的函数: CollectDataToCompare_Fuc.py
'''

import ADTPlan_Args as ADTPA
import ColletDataToCompare_Fuc as CDTCF
import URL_Fuc as URLF
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# key_word to search
key_word = "259luxu"
# local path to search
local_path = "/Volumes/G-RAID Thunderbolt 3/FKT/259luxu大制作/luxu"


if __name__ == '__main__':

    def roll_search(key_Num):
        '''
        确认本地拥有以及缺少的数据
        '''
        # 查找本地拥有的数据
        # 生成listOf_OriginalData
        CDTCF.list_Name_of_files_From(local_path)
        logger.debug("以下为本地库存已经拥有的数据")
        logger.debug(ADTPA.listOf_OriginalData)

        # 生成lsit_num_own(所拥有的数据号);
        # 生成listToDelete(不曾拥有的数据号);
        CDTCF.get_list_of_data_to_delete(
            ADTPA.listOf_OriginalData, key_word, 3)
        logger.debug("以下为本地缺少的数据")
        logger.debug(ADTPA.listToDelete)
        print('以上为本地出错点')
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')


        # arg_to_set:   url, user_agent
        # 设置基本属性之类的头部信息: url ,user_agent


        # 设置搜索的页面数
        page_To_set = 67 # TODO here we need to set
        count_pages_added_one = page_To_set + 1

        list_of_page_args = ADTPA.list_of_page_args
        list_of_page_args = list(range(1, count_pages_added_one))

        # 生成并且处理soup
        for page_args in list_of_page_args:
            print("页数 : 第 " + str(page_args) + "页")
            logger.debug("本次传入的 page_args    ====  %d", page_args)
            str_end_of_url = '/' + str(key_Num) + '/0.html'
            soup = URLF.soup_make_fuc('http://jijibt.com/jiji/' + key_word + '/', str(page_args), str_end_of_url)
            # soup 写入文档保存,用于查找soup出错的原因
            URLF.soup_write_into_txt(soup, page_args)

            # 处理soup并且搜寻关键字,从soup中搜寻关键字
            try:
                ADTPA.Answer_search = soup.body.find(
                    class_="ssbox")
                # 传入比对信息获取需要的磁力链
                CDTCF.findAndCompile_get_magnet()
            except:
                logger.info("第 %s 页的soup有问题", page_args)
        print("总共审查的条数为", ADTPA.count_Num_findAndCompile_get_magnet, "条")


        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')


        # 打印展示本次需要下载的数据
        tag_of_data_need_to_download = sorted(ADTPA.list_of_data_compare_with_listToDelete)
        print("经过比对需要下载总数为", len(tag_of_data_need_to_download), "\n",'经过比对需要下载的数据为: ', tag_of_data_need_to_download )

        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        # logger.debug("listOf_magnent 可能有错误,以下为最后一次listof_magnet版本")
        # logger.debug(ADTPA.listOf_magnet)

        # 将magnet写入到magnet_txt.txt文件中
        with open('magnet_txt.txt', 'w') as magnet_file:
            for magnet in ADTPA.listOf_magnet:
                magnet_file.writelines(magnet + '\n')


    roll_search(2)

    # 遍历所有的搜索逻辑
    # for key_Num in range(6):
    #     roll_search(key_Num)