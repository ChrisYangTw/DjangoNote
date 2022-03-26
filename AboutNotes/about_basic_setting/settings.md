### INSTALLED_APPS
> 在使用資料庫遷移、模板或靜態資源時，會依據該列表順序去查找。


---

### Static files
[參考連結](https://docs.djangoproject.com/zh-hans/4.0/howto/static-files/)
> 用於設定靜態文件的配置。預設會到各app的static資料夾查找檔案，如有設定
> STATICFILES_DIRS 則會先到其指定的位置尋找。
> 
STATIC_URL = 'static/' ，設定靜態文件的url，用於模板語言的 {% load static %}
STATICFILES_DIRS = [ 路徑, ...] ，設置指定查找的優先位置。
---

### Default primary key field type
> 設定models裡每張表的預設主鍵欄位。
> 
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
