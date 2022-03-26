from django.db import models


# Create your models here.
class Upload(models.Model):
    name = models.CharField(verbose_name='上傳者', max_length=32)
    file = models.FileField(verbose_name='檔案', upload_to='reference/upload/file/', null=True, blank=True)
    image = models.ImageField(verbose_name='圖片', upload_to='reference/upload/image/', null=True, blank=True)
    create_time = models.DateTimeField(verbose_name='上傳時間', auto_now_add=True)
