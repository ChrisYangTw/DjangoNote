# Django middleware

___

## process_request

一開始從WSGI server取得HttpRequest後，便從process_request開始處理。  
process_request(self, request)

* 自動給入以下參數  
  * request：HttpRequest物件。
* return
  * 不回傳：自動往下一個process_request或process_view。
  * 回傳HttpResponse物件：將跳過之後的process_view和視圖。往**自身的**process_response開始處理。
    * 如果本身沒定義process_response，則從該中間件的順序，開始回推process_response處理。

___

## process_view

會在調用對應視圖前，先行調用處理。  
process_view(self, request, view_func, view_args, view_kwargs)  

* 自動給入以下參數  
  * request：HttpRequest物件。
  * view_func： 該 url 之 path 調用的視圖。
  * view_args： 該 url 之 path 附帶的位置參數。(如果有)
  * view_kwargs： 該 url 之 path 附帶的關鍵字參數。(如果有)
* return
  * 不回傳：自動往下一個process_view或視圖。
  * 回傳HttpResponse物件：將跳過之後的process_view和視圖。往**全部的**process_response開始處理。
  * 回傳指定的視圖：將跳過之後的process_view，直接調用指定的視圖。  
    * 如要忽略之後的process_view，可直接調用該視圖。

      ```python
      def process_view(self, request, view_func, view_args, view_kwargs):
          pass
          return view_func(*view_args, **view_kwargs)
      ```

    * 也可以調用指定的視圖

      ```python
      from 視圖位置 import 指定的視圖function
      def process_view(self, request, view_func, view_args, view_kwargs):
          pass
          return 指定的視圖function(request)  # 這裡假設該視圖不需參數 
      ```

___

## process_response

不管中間如何處理，最後都透過process_response回傳給WSGI server。  
process_response(self, request, response)

* 自動給入以下參數  
  * request：HttpRequest物件。
  * response： 從view或其他中間件所回傳的HttpResponse。
* return(必須回傳)
  * 回傳HttpResponse物件：往下一個process_response處理。

___

## process_exception

當視圖拋出異常時，方調用。
process_exception(self, request, exception)

* 自動給入以下參數  
  * request：HttpRequest物件。
  * exception： 該 view 所拋出的異常。
* return
  * 不回傳：往下一個process_exception或process_responset處理。
  * 回傳HttpResponse物件：將跳過之後的process_exception。往**全部的**process_response開始處理。

___

## process_template_response()

視圖執行完後，須回HttpResponse物件，當該物件裡有render方法時，方調用。
process_template_response(self, request, response)

* 自動給入以下參數  
  * request：HttpRequest物件。
  * response：從view或其他中間件所回傳之含有render方法的HttpResponse。
* return(必須回傳)
  * 回傳*含有render方法*的HttpResponse物件：往下一個process_template_response或process_response處理。
    * 可於view利用類來封裝，如，

    ```python
    class MyRender:
        def __init__(self, response):
            self.response = response
      
        def render(self):
            return self.response
  
    def view_function(request):
        pass
        response = 你的HttpResponse物件
        return MyRender(response)
    ```
