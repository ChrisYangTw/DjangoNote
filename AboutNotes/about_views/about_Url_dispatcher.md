# 關於URL dispatcher

>使用說明: <https://docs.djangoproject.com/en/4.0/topics/http/urls/>
>相關函數: <https://docs.djangoproject.com/en/4.0/ref/urls/>

## 0. Django處理請求的流程

首先，當我們啟動Django服務後，會根據ROOT_URLCONF的設置，到其對應的.py文件，載入裡面的urlpatterns內容。之後，當有請求傳入時，將該請求所指定的url地址拿來與urlpatterns內容做匹配，如匹配成功則執行相關的視圖。

```python
# settings.py
ROOT_URLCONF = '專案名稱.urls'  # 也就是專案資料夾內的urls.py

# 專案資料夾/urls.py
urlpatterns = [
    ...,
]
```

* 細節
  1. ROOT_URLCONF是可動態改變的。
     * 當HttpRequest有urlconf屬性，則其將會取代原本的ROOT_URLCONF設置。
     * 可通用中間件來實現為HttpRequest添加urlconf屬性。如要恢復原本的ROOT_URLCONF設置，只需再將urlconf屬性設為None即可。
  2. urlpatterns需是django.urls.path()或django.urls.re_path()的實例所組成之序列，通常是用list，以便擴展。
  3. 從HttpRequest的path_info屬性取得url，再拿來和urlpatterns內的每個url規則做匹配，匹配過程是由上而下，一有符合者則停止往下匹配，並調用其對應的視圖。

## 1. 在urlpatterns列表裡使用django.urls提供的函數

### 1.1 path()

>path(route, view, kwargs=None, name=None)
>>route，為匹配url的字串，可搭配路徑轉換器(Path converters)。
>>view，為視圖函數或視圖類(as_view())，也可為django.urls.inclue()的實例。
>>kwargs，可用來傳遞額外的參數給view，通常使用字典。{args1: xxx, args2: xxx, ..}。
>>name，可用來為該條url命名，用於反向解析。

```python
# 範例
urlpatterns = [
    path('admin/', views.admin),
    path('index/', views.index.as_view()),
    path('book/<int:number>/', views.book),
    path('test/', views.test, {'foo': 'bar'}, name='test')
    path('api-auth/', include('rest_framework.urls')),
]
```

#### 1.1.1 內建的路徑轉換器(Path converters)

path()的route參數，即是拿來匹配url的正則(需完全匹配)，如要從url裡取得參數傳遞給對應的視圖，可透過尖括號<參數名稱>，且可使用內建的路徑轉換器來約束該參數可匹配的類型。
|轉換器|可匹配類型|範例|參數類型|
|---|---|---|:---:|
|str|除了'/'之外的非空字串|\<str:name>也可為\<name>|str|
|path|非空字串(含'/')|\<path:name>|str|
|int|0或任何正整数|\<int:name>|==int==|
|slug|slug的格式|\<slug:name>|str|
|uuid|UUID的格式|\<uuid:name>|==UUID物件==|

#### 1.1.2 自訂路徑轉換器

* 步驟
  1. 撰寫自訂的轉換器類(需含下列三項)
     * 名稱為regex的類屬性: 定義用來匹配的正則。
     * to_python(self, value) 方法: 該方法決定要傳給視圖的參數。
     * to_url(self, value) 方法: 反向解析時，該方法決定URL的字串。
  2. 註冊該自訂的轉換器(為該轉換器命名)

```python
# 參考官方範例
# 自訂轉換器類(用來匹配連續4個數字)
class FourDigitYearConverter:
    regex = '[0-9]{4}'
    # 匹配成功的字串，將傳遞給下兩個方法使用(value)

    # 這裡將匹配的字串轉成int類型，所以傳給視圖的參數將會是整數類型
    def to_python(self, value):
        return int(value)

    # 要注意反向解析取得的url一定需為字串類
    def to_url(self, value):
        return '%04d' % value


# 註冊自訂的轉換器
from django.urls import register_converter
# 註冊，並將該轉換器命名為'yyyy'
register_converter(converters.FourDigitYearConverter, 'yyyy')

urlpatters = [
    path('articles/<yyyy:year>', 對應的視圖)
]
```

### 1.2 re_path()

>re_path(route, view, kwargs=None, name=None)
>>參數用法同path()，唯一差別是route需為正則表達式，且不支持路徑轉換器。

```python
# 參考官方範例
urlpatterns = [
    re_path(r'^index/$', views.index, name='index'),
    re_path(r'^bio/(?P<username>\w+)/$', views.bio, name='bio'),
    re_path(r'^blog/', include('blog.urls'))
]
```

對於較複雜的匹配規則，直接使用re_path()通常比使用path()再搭配自訂轉換器來得方便，但要注意的是:

1. 使用re_path()時，須配合使用正則符號'^'和'$'來確保完全匹配。
2. 使用有名分組的方式來實現正則的分組。(雖然可以使用未命名的分組，函數會以位置參數的方式傳遞給對應的視圖，但為了程式的可讀性，應避免這類寫法)
3. 在範例裡的第三條url規則中，其使用了include()來擴展url的匹配，所以該route=r'^blog/'，並未使用'$'來結束匹配。

### 1.3 include()

>include(module, namespace=None)
>include(pattern_list)
>include((pattern_list, app_namespace), namespace=None)

```python
# 參考官方範例
# urls.py
extra_patterns = [
    path('reports/', credit_views.report),
    path('reports/<int:id>/', credit_views.report),
    path('charge/', credit_views.charge),
]

urlpatterns = [
    path('', main_views.homepage),
    path('credit/', include(extra_patterns)),
    path('test/', include([
        path('1/', main_views.test1),
        path('2/', main_views.test2),
        path('3/', main_views.test3),
    ])),
    path('help/', include('help.urls', namespace='help')),
]


# help/urls.py
app_name = help

urlpatterns = [
    path('', help_views.index, name='index'),
    path('comment/', help_views.comment, name='comment'),
]
```

include()搭配path()或re_path()使用，除了可延伸url的匹配，更可增加程式碼的可讀性。