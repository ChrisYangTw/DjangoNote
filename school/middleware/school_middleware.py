from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
import re


class SchoolMiddlewareForCheckLogin(MiddlewareMixin):
    # 當使用者未登入時，無法進入school頁面。(首頁除外)
    # (由於登入及註冊之功能寫在/school/login_register/裡，所以也需避開)
    def process_request(self, request):
        path = request.path_info
        if (
            re.match(r'^/school/.+$', path)
            and '/login_register/' not in path
            and not request.session.get('LOGIN')
        ):
            return redirect('school:login')
