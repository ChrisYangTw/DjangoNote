from django.urls import include, path
from . import views


app_name = 'reference'
urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', include([
        path('file/', views.upload_file, name='upload_file'),
        path('image/', views.upload_image, name='upload_image'),
        path('with_model/', views.upload_with_model, name='upload_with_model'),
        path('delet/<int:nid>/', views.delete_upload_with_model, name='delete_upload_with_model'),
    ])),
]
