from django.urls import path, include
from . import views


app_name = 'school'
urlpatterns = [
    path('', views.index, name='index'),
    path('login_register/', include([
        path('login/', views.login, name='login'),
        path('logout/', views.logout, name='logout'),
        path('register/', views.register, name='register'),
        path('ajax_identify/', views.ajax_get_identify_number_from_sms, name='ajax_get_identify_number_from_sms'),
        path('ajax_verify_code_image', views.ajax_get_verify_code_image, name='ajax_get_verify_code_image'),
    ])),
    path('teacher/', include([
        path('', views.teacher_list, name='teacher_list'),
        path('detail/', views.teacher_detail, name='teacher_detail'),
        path('create/', views.teacher_create, name='teacher_create'),
        path('update/', views.teacher_update, name='teacher_update'),
        path('delete/', views.teacher_delete, name='teacher_delete'),
    ])),
    path('student/', include([
        path('', views.student_list, name='student_list'),
        path('detail/', views.student_detail, name='student_detail'),
        path('create/', views.student_create, name='student_create'),
        path('update/', views.student_update, name='student_update'),
        path('delete/', views.student_delete, name='student_delete'),
    ])),
    path('course/', include([
        path('', views.course_list, name='course_list'),
        path('detail/', views.course_detail, name='course_detail'),
        path('create/', views.course_create, name='course_create'),
        path('update/', views.course_update, name='course_update'),
        path('delete/', views.course_delete, name='course_delete'),
    ])),
    path('accout/', include([
        path('', views.account_list, name='account_list'),
    ]))
]
