import pandas as pd
import json


# 将利润表、资产负债表、现金流量表存储到数据集中  一列列数据存储到dataset里，调用时，需要注意下表格格式 第一列为key值
# 例：
# 姓名  小明   小芳   小雷   小红
# 班级  1   2   3   4
# 课程  语文  数学  英语  美术
# 转成[{姓名：小明，班级：1，课程：语文}，{姓名：小芳，班级：1，课程：数学}]
def dupont_excel_util(path, sheet_name):
    # 读取 Excel 表格
    df = pd.read_excel(path, header=None, sheet_name=sheet_name)
    # 获取第二列及后续列的列名列表
    rows = df.iloc[:, 0].tolist()
    num_columns = len(df.columns)
    # 将表格数据转换为字典列表
    data = []
    for i in range(1, num_columns):
        values = df.iloc[:, i].fillna("").tolist()  # 获取第i列的值，并将空值填充为""
        row_data = {k: v if v else "" for k, v in zip(rows, values)}  # 将空值替换为""
        data.append(row_data)  # 将字典添加到列表
    # 转换为 JSON 字符串
    json_str = json.dumps(data, ensure_ascii=False)

    return json.loads(json_str)


# 将account_fraud课程需要的实验数据转成json
# 例：
# 姓名  班级  课程
# 小明  1   数学
# 小芳  2  英语
# 小红  3  美术
# 转成[{姓名：小明，班级：1，课程：数学}，{姓名：小芳，班级：1，课程：英语}]
def account_fraud_util(path, sheet_name):
    # 读取 Excel 表格
    df = pd.read_excel(path, header=None, sheet_name=sheet_name)
    # 获取列数量
    num_columns = len(df.columns)

    # 将数据转换为JSON格式
    data = []
    # 遍历时去掉第一行数据
    for index, row in df.iloc[1:].iterrows():
        record = {}
        for i in range(num_columns):
            column_name = df.iloc[0, i]  # 获取第一行的值作为列名
            column_value = row[i]
            record[column_name] = column_value
        data.append(record)

    json_data = json.dumps(data, ensure_ascii=False)
    return json.loads(json_data)
