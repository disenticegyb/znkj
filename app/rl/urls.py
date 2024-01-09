from django.urls import path

from app.rl.rl_arima import yc_1

urlpatterns = [
    # 线性分类
    path('yc_1/', yc_1),

]
