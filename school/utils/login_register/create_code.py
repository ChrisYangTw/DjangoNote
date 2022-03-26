"""
可用於產生隨機的驗證碼
參考來源：https://www.cnblogs.com/wupeiqi/acticles/5812291.html
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random


class VerificationCode:
    def __init__(self, width=120, height=30, char_length=5, font_file='Monaco.ttf', only_number=True, noise_level=1):
        self.width = width
        self.height = height
        self.char_length = char_length
        self.font_file = font_file
        self.only_number = only_number
        self.noise_level = noise_level
        self.font_size = int(width/char_length) if width > height else int(height/char_length)

    # 生成隨機字母或數字
    def _rndChar(self):
        if self.only_number:
            return random.choice('0123456789')
        return random.choice('123456789abcdefghijklmnpqrstuvwxyzABCDEFGHIJKLMNPQRSTUVWXYZ')  # 排除0oO避免難以辨識

    # 生成隨機顏色
    def _rndColor(self):
        return random.randint(0, 235), random.randint(0, 235), random.randint(0, 235)  # 刻意避開接近白色(255, 255, 255)

    # 生成隨機字母及其圖片
    def code_image(self):
        code = []
        im = Image.new(mode='RGB', size=(self.width, self.height), color=(255, 255, 255))  # 建一圖片物件作為底圖，顏色為白色
        draw = ImageDraw.Draw(im, mode='RGB')  # 取得繪圖物件
        font = ImageFont.truetype(font=self.font_file, size=self.font_size)  # 選取要使用的字型及大小

        # 先繪製文字
        for i in range(self.char_length):
            random_char = self._rndChar()
            code.append(random_char)
            h = random.randint(-4, 4)  # 隨機生成一個高度，讓寫入字時可有高低不同
            # .text()第一個參數為寫入字的起始左上角座標
            draw.text((i * self.width / self.char_length, h), random_char, font=font, fill=self._rndColor())

        # 繪製干擾
        # 繪製點干擾
        for _ in range(40 * self.noise_level):
            draw.point([random.randint(0, self.width), random.randint(0, self.height)], fill=self._rndColor())
        # 繪製圓圈干擾
        for _ in range(30 * self.noise_level):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            draw.arc([x, y, x + 4, y + 4], 0, 360, fill=self._rndColor(), width=1)
        # 繪製線干擾
        for _ in range(5 * self.noise_level):
            x1 = random.randint(0, self.width)
            y1 = random.randint(0, self.height)
            x2 = random.randint(0, self.width)
            y2 = random.randint(0, self.height)
            draw.line([x1, y1, x2, y2], fill=self._rndColor())

        # 增強圖片
        image = im.filter(ImageFilter.EDGE_ENHANCE_MORE)
        # 回傳code及圖片
        return ''.join(code), image

    def __call__(self):
        return self.code_image()


verification = VerificationCode(char_length=4, noise_level=1)

# if __name__ == '__main__':
#     verification = VerificationCode(char_length=4, noise_level=1)
#     code, im = verification()
#     print(code)
#     im.show()
#     写入文件
#     code, im = verification()
#     with open('code.png','wb') as f:
#         im.save(f,format='png')
#
#     写入内存
#     from io import BytesIO
#     stream = BytesIO()
#     im.save(stream, 'png')
#     stream.getvalue()
