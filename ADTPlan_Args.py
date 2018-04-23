# 数据存放函数

# 以下为处理url,soup的存储
make_url = ''  # 用于存生成的url
list_of_page_args = [] # 用于存储导入的页数, 例如:[1,2,3,4,5,6]

# 以下为用于处理beautifulsoup的存储
Answer_search = None  # 用于临时存储当前的soup搜寻点
listOf_OriginalData = []  # 本地原始数据
list_num_own = []  # 存储拥有的号码
listToDelete = []  # 本库中不存在的数据
listOf_magnet = []  # 存储缺失的磁力链
# 用于临时存储当前页面数据对比listToDelete后所需的数据
list_of_data_compare_with_listToDelete = []
# 用于临时计算本次执行方法的计数
count_Num_findAndCompile_get_magnet = 0

