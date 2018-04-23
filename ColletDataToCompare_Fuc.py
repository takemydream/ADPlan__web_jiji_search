               # 收集信息用于数据比对,下例中收集文件信息
import re
import os
import ADTPlan_Args as ADTPA
import logging


logger = logging.getLogger(__name__)


# 列出所需要的data并且加入到list:listOf_OriginalData中
def list_Name_of_files_From(dir):
    ADTPA.listOf_OriginalData = []
    for name in os.listdir(dir):
        ADTPA.listOf_OriginalData.append(str(name).lower())



# 比对数据的函数,符合B_args的正则就返回True
def fuc_compareData(A_args, B_args):
    if A_args == re.match('(?i)B_args.+'):
        return True

'''
# 截取需要的关键数据段
               #TODO here we need to fix
def get_key_of_data(StringA, string_Key, keep_num_after_key):
    NumArray = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    if "259luxu" in StringA:
        StringB = StringA.split(str(string_Key))[1]
        for Letters in StringB:
            if Letters in NumArray:
                return Letters + StringB.split(Letters)[1][0:keep_num_after_key - 1]
'''
# 截取需要的关键数据段 这里的代码适配性比较差 TODO
def get_key_of_data(StringA, string_Key, keep_num_after_key):

    str_re = '(?i)' + str(string_Key) + '-?\d{' + str(keep_num_after_key) + '}'
    rr = re.compile(str_re)
    group_re_find_all = rr.findall(str(StringA))
    num = int(keep_num_after_key)

    if group_re_find_all != []:
        # 获取数组的元素个数
        num_Len_group_re_find_all = len(group_re_find_all)

        if num_Len_group_re_find_all > 1:
            # 添加一个num在 group_re_find_all 第一位,用来表示数量
            group_re_find_all.insert(0, num_Len_group_re_find_all)
            return group_re_find_all

        elif num_Len_group_re_find_all == 1:
            # 做切割
            StringA_split = str(StringA.split(str(string_Key+"-"))[1]) + "add this words to make sure it will except"
            count_num = 0
            # 上面确保了 执行except,获取从头开始的数字的最后三位
            for StringA_split_son in StringA_split:
                try:
                    int(StringA_split_son)
                    count_num = count_num + 1
                except:
                    StringA_split_last_three_number = StringA_split.split(StringA_split_son)[0][-num:]
                    break
            # 新建list ,包含 1 ,表示只有一个数
            list_a = [1]
            list_a.append(StringA_split_last_three_number)
            return list_a

    elif group_re_find_all == []:
        list_a = [0]
        # 如果没找到re模板的数据,则把原字符串存入列表
        list_a.append(StringA)
        list_a.append(10086)
        return list_a

    else:
        logger.info("意外之外的情况,一般永远不会出现这条错误信息,太可怕了!~")


# 生成一个list用来存剩余需要下载的数据编号
def get_list_of_data_to_delete(data_list, string_Key, keep_num_after_key_of_data):
    num_own = None
    count_error = 0

    for data in data_list:
        # 匹配到的数量
        num_Len_group_re_find_all = get_key_of_data(
            str(data), string_Key, keep_num_after_key_of_data)[0]
        # 附带的信息
        message_group_re_find_all = get_key_of_data(data, string_Key, keep_num_after_key_of_data)[1]

        if num_Len_group_re_find_all == 1:
            num_own = message_group_re_find_all
            try:
                num_own = int(num_own)
            except:
                logger.info("本条数据无法转换为整数: %s", num_own)
            ADTPA.list_num_own.append(num_own)
        else:
            error_message = ''
            if num_Len_group_re_find_all == 0:
                error_message = message_group_re_find_all
            elif num_Len_group_re_find_all > 1:
                error_message = "本条有重复匹配号码:" + str(message_group_re_find_all)

            count_error = count_error + 1
            print('在list_num_own的位置:', num_own, '之后', '出错问题为%s' % error_message)

    print('本地累计出错数量:  ', count_error)
    ADTPA.listToDelete = list(
        set(range(1, 1000)).difference(set(ADTPA.list_num_own)))

    # print("1", ADTPA.list_num_own)
    # print("2", ADTPA.listToDelete)

# 生成本地所有数据集,通过比对爬取的数据,取差集,获取未拥有的磁力链
def findAndCompile_get_magnet():
    # 如果逻辑改变需要更改处理方式
    Answer_search_next = ADTPA.Answer_search.find_next(class_="title")

    ADTPA.Answer_search = Answer_search_next
    # listOf_magnet = ADTPA.listOf_magnet

    # 没找到数据
    if str(Answer_search_next) == 'None':
        print('No More In This Page')

    # 若找到数据进行处理
    else:
        # 比对本地数据文件,查看是否存在这个文件,存在则跳过,不存在则获取magnet并且存到listOf_magnet
        Data_to_compare = get_key_of_data(
            str(Answer_search_next.h3.a.get_text()).lower(), "259luxu", 3)

        # # 将数据由 字符串格式转为整数用于比较
        # try:
        #     Data_to_compare = int(Data_to_compare)
        # except:
        #     logger.info("转换出错了%s", Data_to_compare)

        ADTPA.count_Num_findAndCompile_get_magnet = ADTPA.count_Num_findAndCompile_get_magnet + 1

        num_Len_group_re_find_all = Data_to_compare[0]


        if num_Len_group_re_find_all == 1:
            Data_to_compare_message_hide_in = Data_to_compare[1]
            # 将数据由 字符串格式转为整数用于比较
            try:
                Data_to_compare_message_hide_in = int(Data_to_compare_message_hide_in)
            except:
                logger.info("转换出错了%s", Data_to_compare_message_hide_in)

            if Data_to_compare_message_hide_in in ADTPA.listToDelete:
                ADTPA.list_of_data_compare_with_listToDelete.append(
                    Data_to_compare_message_hide_in)
                ADTPA.listToDelete.remove(Data_to_compare_message_hide_in)
                get_magnet = (Answer_search_next.find_next(
                    href=re.compile('magnet'))).get('href')
                ADTPA.listOf_magnet.append(get_magnet)


    # TODO 以下数据最终需要数据库来存储, 展示
        elif num_Len_group_re_find_all == 0:
            print("没有匹配re模板的,名称为:", Data_to_compare[1])

        elif num_Len_group_re_find_all > 1:
            print('匹配re模板但是同一条信息多数据匹配re模板,数据号为:', Data_to_compare[1:])

        return findAndCompile_get_magnet()
