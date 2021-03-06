# 關於Markdown基本語法

## 1. 標題大小

```text
使用: #加空格再加標題
# 一級標題
## 二級標題
...
###### 六級標題
```
#### 四級標題
###### 六級標題

## 2. 加入程式碼區塊

```text
使用: ```程式語言，如pyhton, java或text。
最後一行使用```，即可結束該程式碼區塊
```
```python
def fn():
    pass
```

## 3. 字體

```text
**加粗字體**
==醒目字體==
~~刪除字體~~
*斜體字體*
```
**加粗字體**
==醒目字體==
~~刪除字體~~
*斜體字體*

## 4. 引用

```text
使用: >開頭，直接加上文字內容。透過多個>可實現階層效果。
>引用ㄧ
>>引用二
>>>引用三
```
>引用ㄧ
>>引用二
>>>引用三

## 5. 分割線

```text
使用: 連續三個減號、星號或底線。
---
***
___
```
---

## 6. 插入圖片

```text
使用: ![圖片描述](圖片連結或檔案路徑)
```
![我的圖片](/Users/chris/Downloads/測試用圖片/學生頭像/121.jpg)

## 7. 加入超連結

```text
使用: [連結描述](連結地址)
```
[google](https://www.google.com/)

## 8. 列表

```text
1. 無序列表
   使用: 星號、加號或減號。
   * 123
   * 456
2. 有序列表
   使用: 數字。
   1. abc
   2. def
3. 有序或無序列表皆可縮排
   使用: 每層空兩格。
   * 1
     * 1-1
     * 1-2
   * 2
     * 2-1
     * 2-2
       * 2-2-1
       * 2-2-2
```
* 123
* 456
1. abc
2. def
* 1
  * 1-1
  * 1-2
* 2
  * 2-1
  * 2-2
    * 2-2-1
    * 2-2-2

## 9. 表格
```text
| 欄位名稱1 | 欄位名稱2 | 欄位名稱3 |
| :--- | :---: | ---: |
| 靠左 | 置中 | 靠右 |
| AAA | BBB | CCC |
```
| 欄位名稱1 | 欄位名稱2 | 欄位名稱3 |
| :--- | :---: | ---: |
| 靠左 | 置中 | 靠右 |
| AAA | BBB | CCC |

## 10. 拖曳字元

```text
使用: 在特殊字元前加上反斜線\。
**123**，為加粗字體。
\*\*123\*\*，可顯示**123**。
```
**123**
\*\*123\*\*
