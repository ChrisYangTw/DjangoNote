from django.db import models


class Courses(models.Model):
    """
    課程：課程名稱、課程學費、開始日期、結束日期、班級人數上限、課程內容說明、授課教師、開課狀態
    """
    class Meta:
        verbose_name = '課程資料'  # 設定在admin管理介面裡的名稱
        verbose_name_plural = '課程資料'  # 設定在admin管理介面裡的名稱(複數時)

    name = models.CharField(verbose_name='課程名稱', max_length=32)
    fee = models.DecimalField(verbose_name='學費', max_digits=7, decimal_places=0, default=0)
    start = models.DateField(verbose_name='開始日期')
    end = models.DateField(verbose_name='結束日期')
    limit = models.PositiveSmallIntegerField(verbose_name='人數上限')
    comment = models.CharField(verbose_name='課程說明', max_length=512, null=True, blank=True)
    teacher = models.ForeignKey(verbose_name='授課教師', to='Teachers', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.BooleanField(verbose_name='開課狀態', default=True)

    def __str__(self):
        return self.name


class Teachers(models.Model):
    """
    師資：教師名稱、性別、相片、每年簽約薪資(授課另計)、加入日期(等同簽約生效日及創立日期)、教師介紹
    """
    class Meta:
        verbose_name = '教師人員'  # 設定在admin管理介面裡的名稱
        verbose_name_plural = '教師人員'  # 設定在admin管理介面裡的名稱(複數時)

    name = models.CharField(verbose_name='教師姓名', max_length=32)
    GENDERS = (
        ('0', '女'),
        ('1', '男'),
        ('2', '保密'),
    )
    gender = models.CharField(verbose_name='性別', choices=GENDERS, max_length=2, default='2')
    # todo: 寫入照片時，在驗證時需處理，1.寫入的轉成需為隨機碼西元年月日小時分秒(兩個隨機字母，湊16字)作為檔名.
    #       2. 利用pillow轉成thumbnail或是其他方式更改大小. 3. 更新照片時，將舊照片刪除
    photo = models.ImageField(verbose_name='相片', upload_to='school/teachers/photo/')
    employment = models.DateField(verbose_name='加入日期', auto_now_add=True)
    salary = models.DecimalField(verbose_name='薪資', max_digits=8, decimal_places=0, default=100000)
    information = models.CharField(verbose_name='教師介紹', max_length=512, null=True, blank=True)

    def __str__(self):
        return self.name


class Students(models.Model):
    """
    學生：學生姓名、性別
    """
    name = models.CharField(verbose_name='學生名稱', max_length=32)
    GENDERS = (
        ('0', '女'),
        ('1', '男'),
        ('2', '保密'),
    )
    gender = models.CharField(verbose_name='性別', choices=GENDERS, max_length=2, default='2')
    photo = models.ImageField(verbose_name='相片', upload_to='school/student/photo/', null=True, blank=True)
    gold = models.DecimalField(verbose_name='儲值金', max_digits=7, decimal_places=0, default=0)
    information = models.CharField(verbose_name='學生介紹', max_length=512, null=True, blank=True)
    course = models.ManyToManyField(verbose_name='參與課程', to='Courses', null=True, blank=True)


class Account(models.Model):
    """
    一般用戶帳號、密碼、手機
    """
    username = models.CharField(verbose_name='使用者帳號', max_length=16)
    password = models.CharField(verbose_name='使用者密碼', max_length=16)
    mobile = models.CharField(verbose_name='使用者電話', max_length=16)
    create_time = models.DateTimeField(verbose_name='創建時間', auto_now_add=True)
