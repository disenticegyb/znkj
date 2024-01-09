import collections
import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

from app.utils.excel_util import account_fraud_util
from app.utils.req_res import handle_exceptions


@csrf_exempt
@require_http_methods(['POST'])
@handle_exceptions
def yc_1(request):
    path = request.POST.get('path') or "templates/test.xlsx"
    sheet_name = request.POST.get('sheet_name') or "Sheet1"
    data = account_fraud_util(path, sheet_name)
    # 坏账  1
    # 不是坏账 2
    # print(type(data))
    # 简单 线性分类预测
    # 特征列  如果为空，则选择全部数据为特征列
    features = request.POST.get('features')
    if features is None:
        first_dict = data[0]
        key_names = list(first_dict.keys())
        features = key_names
    print(features)
    # 目标列 固定为坏账
    target = request.POST.get('target') or "坏账"
    print(target)
    # print(meesge)

    default_values = [item.get(target) for item in data]
    counter = collections.Counter(default_values)
    most_common_types = counter.most_common(2)
    most_common_type_1 = most_common_types[0][0]
    most_common_type_2 = most_common_types[1][0]

    # X = [[d[feature] for feature in features] for d in data]
    # Y = [d[target] for d in data]
    X = []
    Y = []
    # 对于无法转为浮点类型数据，默认处理为0
    for d in data:
        x = [convert_to_float(d[feature]) for feature in features]
        y = convert_to_float(d[target])
        X.append(x)
        Y.append(y)

    # 划分训练集和测试集
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.1, random_state=42)

    # 构建模型
    model = LogisticRegression()

    # 使用训练集进行训练
    model.fit(X_train, Y_train)

    # 使用测试集进行预测
    Y_pred = model.predict(X_test)
    # print(Y_pred)

    # 在测试集上进行评估,评估准确度
    accuracy = model.score(X_test, Y_test)
    print(accuracy)

    classified_data = {
        most_common_type_1: [],
        most_common_type_2: [],
        "未知": []
    }

    # 遍历数据并进行分类
    for i, predicted_label in enumerate(Y_pred):

        # 对数据进行分类  1为真  0为否
        if predicted_label == most_common_type_1:
            classified_data[most_common_type_1].append((most_common_type_1, X_test[i]))
        elif predicted_label == most_common_type_2:
            classified_data[most_common_type_2].append((most_common_type_2, X_test[i]))
        else:
            classified_data["未知"].append(("未知", X_test[i]))
        # print(i)
        # 将样本添加到相应的分类中

    # 分别获取分类结果
    # 构造返回结果的JSON对象
    result = {
        "data1": classified_data[most_common_type_1],
        "data2": classified_data[most_common_type_2],
        "未知": classified_data["未知"],
        # 模型评估准确度
        "accuracy": accuracy,
        # 分类算法结果
        'predictions': Y_pred.tolist()
    }
    result_json = json.dumps(result)
    # 构造 HttpResponse 对象并返回
    response = HttpResponse(result_json, content_type='application/json')
    return response


# 将字符串转换为浮点数的函数，并添加异常处理
def convert_to_float(value):
    try:
        return float(value)
    except ValueError:
        return 0.0
