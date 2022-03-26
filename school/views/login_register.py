"""
登入頁面及註冊面。
應用： 1. 使用ajax技術來處理表單的驗證(暫時使用jQuery，之後可改成fetch來實現)
      2. 使用redis存取驗證碼
"""
from django.shortcuts import render, reverse, redirect
from django.http import JsonResponse, HttpResponse
from io import BytesIO
from school.forms.login_register_forms import RegisterModelForm, CheckMobileNumberForm, LoginForm, LoginWithMobileForm
from school.utils.login_register import get_identify_and_set_cache, verification


def ajax_get_identify_number_from_sms(request):
    """用於手機登入或帳號註冊(模擬手機簡訊取得驗證碼)
    透過Ajax，將表單的手機號碼，透過get方法傳遞。並使用form來驗證，讓所有的異常可透過ValidationError來處理，
    如此方便所有的錯誤訊息可透過.errors來取得。
    """
    # 在html的ajax請求中，加入state的參數，用來處理登入或註冊兩種不同的任務需求。
    # 這裡，如果state不是login或register，則回傳空{}，使頁面無任何反應。
    state = request.GET.get('state')
    if state not in ['login', 'register']:
        return JsonResponse({})

    # 手機號碼校驗，驗證表單需額外傳入state參數。
    check_form = CheckMobileNumberForm(data=request.GET, state=state)
    if check_form.is_valid():
        # 如驗證成功，以{'手機號碼': '隨機驗證碼'}寫入redis(內容僅保留60秒)，隨機驗證碼以JSON格式回傳到前端
        mobile_number = check_form.cleaned_data['mobile']
        identify_number = get_identify_and_set_cache(mobile_number, 6, 60)
        return JsonResponse({'status': True, 'identify_number': identify_number})

    # 驗證失敗則回傳錯誤資訊
    return JsonResponse({'status': False, 'error': check_form.errors})


def ajax_get_verify_code_image(request):
    """用於帳號登入
    取得隨機驗證碼和圖片物件，先使用io模組，將生成的圖片物件暫存在記憶體內，再將驗證碼寫入session中，最終將圖片傳至前端顯示。
    session['CODE'] 將於登入表單驗證時使用。
    """
    code, image = verification()
    stream = BytesIO()
    image.save(stream, 'png')
    request.session['CODE'] = code
    return HttpResponse(stream.getvalue())


def login(request):
    """
    登入頁面，可同時處理使用帳號登入和使用手機登入。
    """
    if request.method == 'POST':
        # 判斷使用者是使用哪種登入方式，再做對應的處理。如有使用者修改javascript，刻意傳送非指定的form_type，將其導向首頁
        form_type = request.POST.get('form_type')
        if form_type not in ['classic', 'phone']:
            data = {'status': 'ignore', 'redirect': reverse('school:index')}
            return JsonResponse(data)

        if form_type == 'classic':  # 使用帳號登入
            bound_form = LoginForm(data=request.POST, request=request)
        else:  # 使用手機登入
            bound_form = LoginWithMobileForm(data=request.POST)

        if bound_form.is_valid():
            # 登入成功後，對session寫入LOGIN和NAME，保留2天。
            # LOGIN，給首頁DjangoNote/index.html的導航欄做不同顯示的邏輯判斷，以及供中間件判斷是否有登入過。
            # NAME，給首頁DjangoNote/index.html顯示的使用者名稱
            request.session['LOGIN'] = True
            request.session['NAME'] = bound_form.cleaned_data['Name']
            request.session.set_expiry(60 * 60 * 24 * 2)
            data = {'status': True, 'redirect': reverse('school:account_list')}
        else:
            data = {'status': False, 'error': bound_form.errors}

        return JsonResponse(data)

    data = {
        'form1': LoginForm(),
        'form2': LoginWithMobileForm(),
    }
    return render(request, 'school/login_register/login.html', data)


def logout(request):
    """
    登出，清除session。導向首頁。
    """
    request.session.flush()
    return redirect('main_index')


def register(request):
    """
    註冊頁面。
    """
    if request.method == 'POST':
        bound_form = RegisterModelForm(data=request.POST)
        if bound_form.is_valid():
            bound_form.save()
            data = {'status': True, 'redirect': reverse('school:login')}
        else:
            data = {'status': False, 'error': bound_form.errors}
        return JsonResponse(data)

    data = {
        'form': RegisterModelForm(),
    }
    return render(request, 'school/login_register/register.html', data)
