#!/usr/bin/python3
# -*- coding: utf-8 -*-


# 發送 Line notify 訊息 


import requests
import os

#from dotenv import load_dotenv


'''
---------------------------------
透過 line notify 的 API 傳送 line 訊息。

send_message : 要傳出去的文字，一定要有訊息才會傳。
token : line notify 的權杖，如果沒有提供，就會使用預設的權杖。
---------------------------------
'''
def line_notify(send_message : str, token:str=None):
    try:
        # 空的就跳出
        if not send_message:
            return

        line_notify_url = 'https://notify-api.line.me/api/notify'

        # 讀取 .env 檔案
        # load_dotenv()
        # line_token = os.getenv('LINE_TOKEN')

        if token:
            line_token = token


        headers = {
            'Authorization': 'Bearer ' + line_token    # 設定權杖
        }

        data = {
            'message': send_message # 設定要發送的訊息
        }

        # data = requests.post(line_notify_url, headers=headers, data=data)   # 使用 POST 方法

    except Exception as e:
        # 顯示錯誤訊息
        print(f"Line notify 發送失敗： {e}")
        # 顯示錯誤的檔案及錯誤的行數
        print(f"錯誤檔案：{e.__traceback__.tb_frame.f_globals['__file__']} 行數：{e.__traceback__.tb_lineno}")            


# 測試 line_notify 是否正常運作
if __name__ == '__main__':
    line_notify('Hello, Line Notify!')
