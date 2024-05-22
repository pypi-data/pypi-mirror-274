import os
import functools
from PIL import Image, ImageFilter, ImageTk, ImageDraw, ImageFont

# 降噪滤波
EMBOSS = ImageFilter.EMBOSS
BLUR = ImageFilter.BLUR
CONTOUR = ImageFilter.CONTOUR
GaussianBlur = ImageFilter.GaussianBlur
SMOOTH = ImageFilter.SMOOTH
FIND_EDGES = ImageFilter.FIND_EDGES

# 冲采样滤波
BICUBIC = Image.BICUBIC
LANCZOS = Image.LANCZOS
NEAREST = Image.NEAREST
BILINEAR = Image.BILINEAR

# 图像翻转形式
FLIP_LEFT_RIGHT = Image.FLIP_LEFT_RIGHT
FLIP_TOP_BOTTOM = Image.FLIP_TOP_BOTTOM
ROTATE_90 = Image.ROTATE_90
ROTATE_180 = Image.ROTATE_180
ROTATE_270 = Image.ROTATE_270
TRANSPOSE = Image.TRANSPOSE
TRANSVERSE = Image.TRANSVERSE

# 图片变化方式
EXTENT = Image.EXTENT


def change(img):
    """
    转换图像为tk可用格式
    :param img: Image对象
    :return:
    """
    return ImageTk.PhotoImage(img)


class ZybImage:

    def __init__(self, im):
        self.__im = im

    def __getattr__(self, item):
        attr = getattr(self.__im, item)
        if callable(attr):
            @functools.wraps(attr)
            def function(*args, **kwargs):
                obj = attr(*args, **kwargs)
                if isinstance(obj, Image.Image):
                    return ZybImage(obj)
                return obj
            return function
        return attr

    def draw_text(self, text, xy=(0, 0), size=16, fill=(255, 255, 255), font=None):
        """
        在图像上添加文本
        :param xy: 图像坐标(x, y)
        :param text: 绘制文本
        :param font: 文本字体
        :param size: 文字大小
        :param fill: 文字颜色
        """
        if not font:
            font_path = os.path.join(os.path.dirname(__file__), "assets/HYShangWeiXiaoShiHouJ.ttf")
        else:
            font_path = font

        if not os.path.exists(font_path):
            raise ValueError("找不到指定的字体")
        font_size = size
        font = ImageFont.truetype(font_path, font_size)

        draw = ImageDraw.Draw(self.__im)
        draw.text(xy, text, font=font, fill=fill)
        return self


def open(fp, formats=None):
    """打开图片"""
    im = Image.open(fp, formats=formats)
    if not im:
        return im
    return ZybImage(im)


__all__ = ["open",
           "EMBOSS", "BLUR", "CONTOUR", "GaussianBlur", "SMOOTH", "FIND_EDGES",
           "BICUBIC", "LANCZOS", "NEAREST", "BILINEAR",
           "FLIP_LEFT_RIGHT", "FLIP_TOP_BOTTOM", "ROTATE_90", "ROTATE_180", "ROTATE_270", "TRANSPOSE", "TRANSVERSE",
           "EXTENT"]



