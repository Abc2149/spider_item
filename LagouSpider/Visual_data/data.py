import pymysql
from collections import Counter
from pyecharts import Bar,Pie,WordCloud

# 连接mysql
db = pymysql.Connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    passwd='root',
    db='lagouspider',
    charset='utf8',
)
# 操作游标
cursor = db.cursor()
'''
# 工作经验
workYear_sql = "select workYear from lagou"
cursor.execute(workYear_sql)
# 返回查询到的所有记录，并去重
workYear_data = set(cursor.fetchall())
# print(workYear_data)
workYear_list = [i[0] for i in workYear_data]
# 统计workYear字段的字段值出现的次数
workYear_count = []
for each in workYear_list:
    sql = "select * from lagou where workYear = '%s'" %each
    cursor.execute(sql)
    count = cursor.rowcount   # 记录查询了多少行
    workYear_count.append(count)
# print(workYear_count)
'''

def getdata(filed):
    sql = "select %s from lagou" % filed
    cursor.execute(sql)
    # 返回查询到的所有记录(元组类型)
    data = cursor.fetchall()
    # 统计相同字段值出现的次数
    count = dict(Counter(each[0] for each in data))     # {'本科'：44}
    # 画图的数据为列表形式
    data_list = list(count.keys())
    # 统计字段出现的次数
    data_count = [count[i] for i in data_list]
    return data_list,data_count

education_list,education_count = getdata('education')           # 教育程度
district_list,district_count = getdata('district')              # 地区
positionName_list,positionName_count = getdata('positionName')  # 职位
workYear_list,workYear_count = getdata('workYear')              # 工作年限
salary_list,salary_count = getdata('salary')                    # 薪资

# 柱状
bar = Bar('工作区域','')
bar.add('',district_list,district_count)
bar.show_config()
bar.render('district.html')

# 饼图
pie = Pie('教育程度','')
pie.add('',education_list,education_count,is_label_show=True)
pie.show_config()
pie.render('education.html')

# 词云
wordcloud = WordCloud(width=1000,height=620)
wordcloud.add('',salary_list,salary_count,word_size_range=[30,100])
wordcloud.show_config()
wordcloud.render('salary.html')








