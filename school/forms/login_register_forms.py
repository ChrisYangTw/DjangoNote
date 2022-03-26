from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
from school.models import Account
from school.utils.login_register.set_cache import Conn


class RegisterModelForm(forms.ModelForm):
    """
    註冊頁面使用，配合model。
    """
    username = forms.CharField(label='使用者帳號',
                               max_length=16,
                               min_length=4,
                               widget=forms.TextInput(attrs={'placeholder': '請輸入帳號'}))

    password = forms.CharField(label='使用者密碼',
                               max_length=16,
                               min_length=4,
                               widget=forms.PasswordInput(attrs={'placeholder': '請輸入密碼'}))

    password_reply = forms.CharField(label='再次輸入密碼',
                                     max_length=16,
                                     min_length=4,
                                     widget=forms.PasswordInput(attrs={'placeholder': '請再次輸入密碼'}))

    mobile = forms.RegexField(label='手機號碼',
                              regex=r'^\d{10}$',
                              widget=forms.TextInput(attrs={'placeholder': '輸入手機號碼(十碼)'}),
                              error_messages={'invalid': '手機號碼格式錯誤'})

    identify = forms.RegexField(label='驗證碼',
                                regex=r'^\s*\d{6}\s*$',
                                widget=forms.TextInput(attrs={'placeholder': '驗證碼'}),
                                error_messages={'invalid': '驗證碼格式錯誤'},
                                strip=True)  # 允許使用者輸入時前後有空格

    class Meta:
        model = Account
        fields = ['username', 'password', 'password_reply', 'mobile', 'identify']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

    def clean_username(self):
        username = self.cleaned_data['username']
        if Account.objects.filter(username=username).exists():
            raise ValidationError('該用戶帳號已被使用')
        return username

    def clean_password_reply(self):
        # 為何取得password需使用.get()？因為要考慮到password欄位可能沒輸入，導致cleaned_data裡面沒資料;
        # 而走到clean_password_reply時，代表password_reply欄位初步驗證(不可為空)已經通過，所以cleaned_data裡已有資料。
        password = self.cleaned_data.get('password')
        password_replay = self.cleaned_data['password_reply']
        if password != password_replay:
            raise ValidationError('前後密碼不一致')
        return password_replay

    def clean_mobile(self):
        mobile_number = self.cleaned_data['mobile']
        if Account.objects.filter(mobile=mobile_number).exists():
            raise ValidationError('手機號碼已存在')
        return mobile_number

    def clean_identify(self):
        mobile_number = self.cleaned_data.get('mobile')
        # 如果手機號碼為空，觸發ValidationError，但不需在其span顯示錯誤訊息，因為mobile的span會顯示錯誤訊息。
        if not mobile_number:
            raise ValidationError('')

        # 從redis裡取得驗證碼，如果無法取得(已失效)，則identify_number=None，不進行解碼。
        identify_number = Conn.get(mobile_number)
        if identify_number:
            identify_number = identify_number.decode('utf-8')
        # 驗證是否相同。
        identify = self.cleaned_data['identify'].strip()
        if identify_number != identify:
            raise ValidationError('驗證碼錯誤或失效')

        return identify


class CheckMobileNumberForm(forms.Form):
    """
    用來驗證是否為手機號碼格式，可分別處理是要用來登入或是用來註冊。
    登入時，手機號碼需在資料庫內;而註冊時，則不可在資料庫內。(用clean鉤子函數來實現)
    """
    mobile = forms.RegexField(label='手機號碼',
                              regex=r'^\d{10}$',
                              widget=forms.TextInput(attrs={'placeholder': '輸入手機號碼(十碼)'}),
                              error_messages={'invalid': '手機號碼格式錯誤'})

    def __init__(self, *args, state, **kwargs):
        super().__init__(*args, **kwargs)
        # 只需判斷一次即可，因為我們傳入的state不是 'login' 就是 'register'。
        self.state = state == 'login'

    def clean_mobile(self):
        mobile_number = self.cleaned_data['mobile']

        if self.state:  # 登入使用時
            if not Account.objects.filter(mobile=mobile_number).exists():
                raise ValidationError('請確認手機號碼是否正確')
        elif Account.objects.filter(mobile=mobile_number).exists():  # 註冊使用時
            raise ValidationError('手機號碼已經被使用')
        return mobile_number


class LoginForm(forms.Form):
    """
    帳號登入用表單
    """
    username = forms.CharField(label='帳號')
    password = forms.CharField(label='密碼', widget=forms.PasswordInput)
    code = forms.RegexField(label='驗證碼',
                            regex=r'^\s*\d{4}\s*$',
                            error_messages={'invalid': '請輸入4個數字'})

    # 在驗證時，我們需要用到request，但在生成表單時，我們想省去需傳入request，所以設定參數request=None
    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control', 'placeholder': f'請輸入{field.label}'})
            if name == 'username':
                field.widget.attrs.update({'placeholder': '請輸入帳號(可用電話號碼)'})

    def clean_password(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data['password']
        # 可使用帳號或手機號碼來登入
        account = Account.objects.filter(Q(username=username) | Q(mobile=username)).filter(password=password)
        if not account.exists():
            raise ValidationError('帳號或密碼錯誤')
        self.cleaned_data['Name'] = account.first().username  # 這裡另外加入'Name'的資料，為了配合使用手機登入後，也可以將使用者資料寫入session
        return password

    def clean_code(self):
        input_code = self.cleaned_data['code']
        session_code = self.request.session.get('CODE')
        if not session_code:
            raise ValidationError('驗證碼過期')
        if input_code != session_code:
            raise ValidationError('驗證碼錯誤')
        return input_code


class LoginWithMobileForm(forms.Form):
    """
     電話登入表單
    """
    mobile = forms.RegexField(label='電話號碼',
                              regex=r'^\d{10}$',
                              widget=forms.TextInput(attrs={'placeholder': '輸入註冊之手機號碼'}),
                              error_messages={'invalid': '請輸入手機號碼'})
    identify = forms.RegexField(label='輸入驗證碼',
                                regex=r'^\s*\d{6}\s*$',
                                error_messages={'invalid': '請輸入6個數字'},
                                strip=True)  # 允許使用者輸入時前後有空格

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

    def clean_mobile(self):
        mobile_number = self.cleaned_data['mobile']
        if not Account.objects.filter(mobile=mobile_number).exists():
            raise ValidationError('請確認手機號碼是否正確')
        # 為了在login_register.py裡的login函數，可使用較少的程式碼，將使用者資料寫入session。所以在cleaned_data加入使用者名稱。
        self.cleaned_data['Name'] = Account.objects.filter(mobile=mobile_number).first().username
        return mobile_number

    def clean_identify(self):
        mobile_number = self.cleaned_data.get('mobile')
        # 如果手機號碼為空，觸發ValidationError，但不需在其span顯示錯誤訊息，因為mobile的span會顯示錯誤訊息。
        if not mobile_number:
            raise ValidationError('')

        # 從redis裡取得驗證碼
        identify_number = Conn.get(mobile_number)
        if identify_number:
            identify_number = identify_number.decode('utf-8')
        # 驗證是否相同
        identify = self.cleaned_data['identify']
        if identify_number != identify:
            raise ValidationError('驗證碼錯誤或失效')

        return identify
