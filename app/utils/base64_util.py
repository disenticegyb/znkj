import base64
from io import BytesIO


def save_image_to_base64(fig):
    # 保存图像到字节流
    fig_bytes = BytesIO()
    fig.savefig(fig_bytes, format='png')
    fig_bytes.seek(0)

    # 将图像转换为Base64编码
    fig_base64 = base64.b64encode(fig_bytes.getvalue()).decode('utf-8')

    # 关闭字节流
    fig_bytes.close()

    if hasattr(fig, 'close') and callable(getattr(fig, 'close')):
        fig.close()

    # 构造结果字典并转换为JSON
    return fig_base64


def cover_base64_to_image(base64_str):
    return 'data:image/png;base64,' + str(base64_str)


def base64_img_json(base64_str):
    result = {
        'image': cover_base64_to_image(base64_str)
    }
    return result
