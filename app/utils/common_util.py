import os
import random
import string

# 获取k长度的随机字符串
import numpy as np
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from app.utils.model_util import get_exp_model
from app.utils.req_res import handle_exceptions, parse_request_data


def get_random_string(k):
    # 生成数字、大小写字母的字符集
    characters = string.digits + string.ascii_letters

    # 随机生成6位字符串
    random_str = ''.join(random.choices(characters, k=k))
    return random_str


# 获取表格名字
def get_excel_name(path):
    filename = os.path.basename(path)

    # 去掉文件后缀名
    filename_without_extension = os.path.splitext(filename)[0]

    profit_statement_name = filename_without_extension

    return profit_statement_name


# 打分实验分数
@csrf_exempt
@require_http_methods(['POST'])
@handle_exceptions
def get_exp_score(request):
    request_data, model = parse_request_data(request)
    # 获取实验总分
    total = request_data.get('total') or 100
    # 获取实验模型
    if hasattr(model, "model"):
        new_model = model.model["value"]
    else:
        new_model = None
    # 评分标准  模型拟合度评估占比30%   对象属性值比对占比70%
    # 80分以上  25-30%
    # 60-80分  20-25%
    # 60分一下或者空  10%-20%
    # 模型为空给10-20%的分值
    if new_model is None:
        # 只计算对象的相似度
        model_score = 0
        model_answer = get_exp_model(request_data)
        if model_answer is None:
            return 0
        # 没有模型则只计算model属性
        else:
            exp_score = answer_score(model, model_answer, total, 1)
    else:
        # 残差分析
        residuals = new_model.resid
        # 均方根误差
        rmse = np.sqrt(np.mean(residuals ** 2))
        model_score = calculate_score(rmse, total)
        model_answer = get_exp_model(request_data)
        exp_score = answer_score(model, model_answer, total, 0.7)
    return exp_score + model_score


def calculate_score(rmse, total):
    normalized_mse = (rmse - 0.5) / 1.5
    score = 100 * (1 - normalized_mse)
    if score >= 80:
        return int(random.uniform(0.25, 0.3) * total)
    elif score >= 60:
        return int(random.uniform(0.2, 0.25) * total)
    else:
        return int(random.uniform(0.1, 0.2) * total)


# 标准答案与实际答题打分
def answer_score(new_model, answer_model, total, coe):
    # 对象长度相似度占比70%
    proper_len = compare_len(new_model, answer_model) * coe * 0.7 * total
    # 属性长度比较
    value_len = compare_value(new_model, answer_model) * coe * 0.3 * total
    return int(value_len + proper_len)


# 对象长度相似度占比70%
def compare_len(class1, class2):
    attr_count1 = len(class1.__dict__)
    attr_count2 = len(class2.__dict__)
    similarity_score = (min(attr_count1, attr_count2) / max(attr_count1, attr_count2))
    return similarity_score


# 对象内容长度相似度占比30%
def compare_value(class1, class2):
    attr_names1 = class1.__dict__.keys()
    attr_names2 = class2.__dict__.keys()

    common_attr_names = set(attr_names1) & set(attr_names2)
    total_common_attrs = len(common_attr_names)

    similarity_score = 0

    for attr_name in common_attr_names:
        value1 = class1.__dict__.get(attr_name)
        value2 = class2.__dict__.get(attr_name)
        if value1 is not None and value2 is not None:
            length1 = len(str(value1))
            length2 = len(str(value2))
            ratio = min(length1, length2) / max(length1, length2)
            if 0.8 <= ratio <= 1.2:
                similarity_score += 1
    similarity_score = (similarity_score / total_common_attrs)
    return similarity_score
