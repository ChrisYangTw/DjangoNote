"""DjangoNote URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),  # 尚未未實現
    path('', views.index, name='main_index'),
    path('test/', views.test, name='main_test'),
    path('reference/', include('reference.urls', namespace='reference')),
    path('school/', include('school.urls', namespace='school')),
]

if settings.DEBUG:
    # debug模式下，django自帶的服務器只會幫忙處理靜態文件，但media的部分，我們需自行設定
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # 非debug模式時，可暫時使用django提供的檔案伺服器，來幫助我們取得資源(靜態文件及media)。
    from django.views.static import serve

    urlpatterns.extend([
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    ])
