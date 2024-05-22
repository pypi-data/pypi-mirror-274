from PIL import Image


class ZybImage:

    def __init__(self, img):
        self._img = img

    @staticmethod
    def open(self, filename):
        img = Image.open(filename)
        return ZybImage(img)

    @property
    def width(self):
        return self._img.width

    @property
    def height(self):
        return self._img.height

    @property
    def size(self):
        return self._img.size

    @property
    def format(self):
        return self._img.format

    def load(self):
        return self._img.load()

    def show(self):
        self._img.show()

    def save(self, filename, format=None):
        """
        图像保存
        :param filename: 字符串，文件名， 必填
        :param format: 字符串，图像格式，选填
        :return: None
        """
        self._img.save(filename, format=format)

    def resize(self, size, resample=Image.BICUBIC):
        """
        图像缩放
        :param size: 元组，缩放尺寸
        :param resample: 选填，图像采样滤波器
        :return: 图像对象
        """
        self._img.resize(size, resample=resample)

    def convert(self, mode):
        """
        图像色彩模式转换
        :param mode: 字符串，色彩模式， 'L'为灰度模式，'RGB'为真彩模式，'CMYK'为色彩模式
        :return: 图戏对象
        """
        self._img.convert(mode=mode)
        return self

    def filter(self, filter):
        """
        图像过滤
        :param filter: 过滤器
        :return: self
        """
        self._img.filter(filter=filter)
        return self

    def rotate(self, angle, resample=Image.NEAREST):
        """
        图像旋转
        :param angle: 数字，旋转角度
        :param resample: 采样滤波器，选填
        :return:
        """
        self._img.rotate(angle, resample=resample)
        return self

    def crop(self, box=None):
        """
        图像裁剪
        :param box: 剪裁区域，四数字的元祖
        :return: self
        """
        self._img.crop(box)
        return self

    def copy(self):
        img = self._img.copy()
        return ZybImage(img)

    def paste(self, image):
        if isinstance(image, ZybImage):
            self._img.paste(image._img)
        else:
            self._img.paste(image)

    def thumbnail(self, size, resample=Image.BICUBIC):
        """
        图像缩略图
        :param size: 元祖，图像缩略图大小
        :param resample: 图像采样率
        :return:
        """
        self._img.thumbnail(size, resample=resample)
        return self

    def transpose(self, method):
        """
        图像翻转
        :param method: 图片翻转形式
        :return:
        """
        self._img.transpose(method)
        return self

    def transform(self, size, method):
        """
        图像变换
        :param size: 元祖，新图像大小
        :param method: 图像变化方式
        :return:  self
        """
        self._img.transform(size, method)
        return self


open = ZybImage.open

