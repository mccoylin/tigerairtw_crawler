#!/usr/bin/python3
# -*- coding: utf-8 -*-


# 虎航「特別優惠」 特價網址爬蟲
# 爬蟲完成時間：2024/09/24
# 若網頁改版，就需要重新分析網頁的資料格式，並修改程式碼。
#
# request.get() 就能取得特價資料


import requests
from bs4 import BeautifulSoup
import re
import datetime

# 自訂模模：發送訊息到 line notify 的模組
from line_notify import line_notify     


def tiger_air_tw() -> list:
    # {
    try:
        # {
        # 虎航特價網址, 用 get 是取到資料的
        headers_firefox = { 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0' }
        headers_chrome  = { 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36' }
        url = 'https://www.tigerairtw.com/zh-tw/ready-to-go/special-offers'

        res = requests.get(url, headers=headers_chrome) 
        soup = BeautifulSoup(res.text, 'html.parser')

        # print(soup.prettify())

        # # 這裡是把網頁存起來, 之後可以用瀏覽器打開看看
        # with open('tiger.html', mode="w") as file:
        #     file.write(soup.prettify()) 

        # 特價的訊息是在 window.__NUXT__ = { ... } 這個 javascript 物件裡面
        # 試過 json.loads(), BeautifulSoup 都無法解析, 所以只好用正規表示法, 來取出這個物件
        journey_pattern = re.compile(r'window.__NUXT__.*')

        result = journey_pattern.search(soup.prettify())
        if not result:
            return None

        journey_json = result.group()

        # HTML 裡的長相
        # function(a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z,A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z,_,$,aa,ab,ac,ad,ae,af,ag,ah,ai,aj,ak,al,am,an,ao,ap,aq,ar,as,at,au,av,aw,ax,ay,az,aA,aB)
        # 取出 function 的參數名稱，要用來組合出正確的參數內容。
        function_pattern = re.compile(r'function\((.*)\)\{')       
        result_function = function_pattern.search(journey_json)
        if result_function:
            function_params = result_function.group(1).split(',')       # 切出參數名稱
            # print(function_params)

        # 取出 parameter 的資料
        # 參數的長相
        # serverRendered:aB}}       # 前一段的結尾，後面直接接傳入的參數
        # ("text","",null,"\u003Cp\u003E2024\u002F03\u002F31-2025\u002F03\u002F29\u003C\u002Fp\u003E","button","尋找航班","2020\u002F03\u002F29 - 2020\u002F10\u002F24","\u003Cp\u003E2024\u002F03\u002F31-2024\u002F10\u002F26\u003C\u002Fp\u003E","2019\u002F10\u002F04 1000 - 2020\u002F10\u002F24 2359","2019\u002F10\u002F01 1000 - 2020\u002F10\u002F24 2359","旅遊日期","\u003Cp\u003ETWD 3299+\u003C\u002Fp\u003E","\u003Cp\u003E2024\u002F07\u002F01-2024\u002F08\u002F31\u003C\u002Fp\u003E","票價","開票日期","\u003Cp\u003ETWD 2399+\u003C\u002Fp\u003E","高雄往","台中往","1699","1999","\u003Cp\u003ETWD 1699+\u003C\u002Fp\u003E","1799","\u003Cp\u003ETWD 2199+\u003C\u002Fp\u003E","\u003Cp\u003E東京成田\u003C\u002Fp\u003E","\u003Cp\u003E名古屋\u003C\u002Fp\u003E","\u003Cp\u003E2024\u002F01\u002F18 - 2025\u002F03\u002F29\u003C\u002Fp\u003E","台北(桃園) 往","table","searchTable","尋找航班 ","destination","\u003Cp\u003E澳門\u003C\u002Fp\u003E","billing_date","price","params","defaultTable","\u003Cp\u003ETWD 1199+\u003C\u002Fp\u003E","\u003Cp\u003ETWD 1799+\u003C\u002Fp\u003E","travel_date","\u003Cp\u003ETWD 2699+\u003C\u002Fp\u003E","collapseBox","澳門","MFM","2199","zh-tw","\u003Cp\u003ETWD 3799+\u003C\u002Fp\u003E","台北(桃園)往","1299","\u003Cp\u003ETWD 2499+\u003C\u002Fp\u003E","大阪","\u003Cp\u003E沖繩\u003C\u002Fp\u003E","\u003Cp\u003E峴港\u003C\u002Fp\u003E","KIX","福岡","FUK","名古屋","\u003Cp\u003E福岡\u003C\u002Fp\u003E","NGO","\u003Cp\u003E大阪\u003C\u002Fp\u003E","特別優惠","東京成田","\u003Cp\u003ETWD 1999+\u003C\u002Fp\u003E","NRT","沖繩","OKA","HKD","899","en","\u003Cp\u003E釜山\u003C\u002Fp\u003E","jp","kr","th","vn","special-offers","faq","常見問題","contact-us","聯繫我們","語言","TWD","0",true));
        param_pattern = re.compile(r'serverRendered:aB\}{2}\((.*)\){2};')
        result_param = param_pattern.search(journey_json)
        if result_param:
            # print(result_param.group(1))
            param_data = result_param.group(1).split(',')

        # 組合 function_params 及 param_data, 方便後續取用
        # print(f'{len(function_params)},  {len(param_data)}')
        if result_function and result_param:
            param_dict = dict(zip(function_params, param_data))     # 組合成 dict，後續用 key, value 簡單配對取出
            # 資料有 unicode 符號，先還原再移除<p>標籤，也一併移除雙引號
            for key, value in param_dict.items():
                value = value.replace(r'\u003C', r'<').replace(r'\u003E', r'>').replace(r'\u002F', r'/').replace(r'"', r'') 
                value = value.replace(r'<p>', r'').replace(r'</p>', r'')
                # print(f'{key} = {value}')
                param_dict[key] = value

        # return 段的真實長相
        # {return {layout:"default",data:[{pageName:af,components:[{type:a,content:   ...中間省略... 
        # ,serverRendered:aB}}          # 結尾的特徵
        # 取出 return 的資料，這裡是行程的所有資料。
        return_pattern = re.compile(r'\{return\s({.*serverRendered:aB\})\}')   
        result_return = return_pattern.search(journey_json)
        if not result_return:
            return None
        return_data = result_return.group(1)

        # 手動分析時，發現資料的格式是這樣的。剛好是網頁的 columns 資料，一共會出現有三個區段。符合台北，台中，高雄三個區段
        # {key:c,label:A},  A = "台北(桃園) 往"     # 出發地
        # {key:c,label:k},  k = "旅遊日期"
        # {key:c,label:o},  o = "開票日期"
        # {key:c,label:n},  n = "票價"
        # {key:c,label:c}   c = null        # 超連結的按鈕
        found_pattern = re.compile(r'\{key:\w,label:(\w)\},\{key:\w,label:\w\},\{key:\w,label:\w\},\{key:\w,label:\w\},\{key:\w,label:\w\}')            
        found_end_pattern = re.compile(r'\]\}\}\]\}\}')            #  區塊結尾的特微，用來切割資料尾部。

        # 找出所有的行程資料，應該有台北，台中，高雄三個區段，airport_list 用來存放這三個區段的起飛機場資料
        # 起飛機場應該是參數名稱，所以要用 param_dict 裡面的資料取代
        airport_list = found_pattern.findall(return_data)
        if 0 ==  len(airport_list):
            return None
        print(f"airport_list = {len(airport_list)}, {airport_list}")

        # 用 found_pattern 依起飛機場別，切割出特價的資料
        found_list = (re.split(found_pattern, return_data)[1:])   # 第一個沒有需要的資料，拋棄
        found_list = [re.split(found_end_pattern, found)[0] for found in found_list]        # 用 found_end_pattern 來分割時，[0] 是要保留的資料，切割後的資料是 list[] 的格式，丢棄後面不需要的資料
        # 還原 unicode 特殊符號，也加上換行符號，這樣比較容易加工。正確性也會提高。
        found_list = [found.replace(r'\u003C', r'<').replace(r'\u003E', r'>').replace(r'\u002F', r'/').replace(r'}]},', r'}]}\r') for found in found_list]        # 用 found_end_pattern 來分割時，[0] 是要保留的資料

        # # 驗證取出的資料
        # for found in found_list:
        #     print(f"found_list = {len(found)}")
        #     print(f"{found}")
        #     print('-----')

        # 每筆特價資料的長相
        # [{components:[{type:a,content:"\u003Cp\u003E函館\u003C\u002Fp\u003E"}]},{components:[{type:a,content:d}]},{components:[{type:a,content:d}]},{components:[{type:a,content:l}]},{components:[{type:e,content:f,image_url:b,url:"https:\u002F\u002Fbooking.tigerairtw.com\u002Fzh-TW\u002Findex?type=roundTrip&outbound=TPE-HKD&inbound=HKD-TPE&departureDate=&returnDate&adult=1&children=0&infant=0&affiliateChannel=specialoffers_zhtw",color:b}]}]
        # re pattern 太長，取不出來....
        # airplane_pattern = re.compile(r'\[\{components:\[\{type:\w,content:.+\}\]\},\{components:\[\{type:\w,content:.+\}\]\},\{components:\[\{type:\w,content:.+\}\]\},\{components:\[\{type:\w,content:.+\}\]\},\{components:\[\{type:\w,content:.+,image_url:\w,url:".+",color:\w\}\]\}\],?')
        airplane_part_pattern = re.compile(r'\{components:\[\{type:\w,content:(.*?)\}\]\},?')
        airplane_url_pattern = re.compile(r'url:"(.*)"')        # 取出超連結的網址

        airplane_list = []
        for airport in found_list:
            patr_data = airplane_part_pattern.findall(airport) 
            if not len(patr_data) or len(patr_data) % 5 != 0:       # 如果沒有找到行程資料，或是資料不是 5 的倍數，就不處理
                continue
            print(f"patr_data = {len(patr_data)/5} 筆資料")

            travel_list = []
            # 一次從 part_data 取出 5 筆資料，組合成一筆行程資料
            for i in range(0, len(patr_data), 5):
                travel_dict = {
                    'destination' : patr_data[i].replace(r'<p>', r'').replace(r'</p>', r''),
                    'travel_date' : patr_data[i+1].replace(r'<p>', r'').replace(r'</p>', r''),
                    'billing_date' : patr_data[i+2].replace(r'<p>', r'').replace(r'</p>', r''),
                    'price' : patr_data[i+3].replace(r'<p>', r'').replace(r'</p>', r''),
                    'url' : airplane_url_pattern.search(patr_data[i+4]).group(1) if airplane_url_pattern.search(patr_data[i+4]) else ''
                }
                travel_list.append(travel_dict)     # 每筆行程資料加入 list
            # print(travel_list)
            airplane_list.append(travel_list)       # 每個機場的行程資料加入 list

        # 取出所有需要的資料後，就可以把資料整理成需要的格式。尤其是把參數名稱還原成正確的資料。
        # 機場名稱還原
        for airport in airport_list:
            if airport in param_dict.keys():
                airport_list[airport_list.index(airport)] = param_dict[airport].replace(r'"', r'')

        date_pattern = re.compile(r'(\d{4}\/\d{2}\/\d{2})')    # 取出日期
        # 處理行程資料裡面的 params, 如果該被取代，套用 param_dict 裡面的資料
        for airport_index, airport in enumerate(airplane_list):
            for travel in airport:
                for key, value in travel.items():
                    value = value.replace(r'"', r'')        # 去掉多餘的'"'符號
                    # 如果 value 該被取代
                    if value in param_dict.keys():      
                        # print(f"travel[{key}] : {value}")
                        value = param_dict[value].replace(r'"', r'')
                    # 整理日期格式 “％Y％m%d - %Y%m%d”
                    if key == 'travel_date' or key == 'billing_date':
                        date1 = date_pattern.findall(value)
                        value = f"{date1[0]} - {date1[1]}"
                    travel[key] = value.replace(r'"', r'')
                travel['departure'] = airport_list[airport_index].replace(r'往', r'').strip()   # 加上出發地資料，去掉"往"字，並去掉空白
                #travel['destination'] = airport_list[airport_index] + travel['destination'].replace(r'"', r'')

        # 把airplane_list行程資料組合成 list[] 的格式
        airplane_list = [travel for airport in airplane_list for travel in airport]

        # print(airplane_list)
        print(f'一共爬取 {len(airplane_list)} 筆資料')

        return airplane_list 

        # }         # End of try

    except Exception as e:
        # 顯示錯誤訊息
        print(f"tiger_air_tw() 出現錯誤: {e}")
        # 顯示錯誤的檔案及錯誤的行數
        print(f"錯誤檔案：{e.__traceback__.tb_frame.f_globals['__file__']} 行數：{e.__traceback__.tb_lineno}")            

        return None

    # }     # End of tiger_air_tw() -> list:




if __name__ == '__main__':
    try:
        travel_list = tiger_air_tw()

        date_pattern = re.compile(r'(\d{4}\/\d{2}\/\d{2})')    # 取出日期
        for travel in travel_list:
            # 排除開票時間過期的資料
            date1 = date_pattern.findall(travel['billing_date'])
            billing_end = datetime.datetime.strptime(date1[1], '%Y/%m/%d').date()
            if billing_end < datetime.datetime.now().date():
                print(f"{travel['departure']} - {travel['destination']}，開票期限 {travel['billing_date']} 已逾期，不予處理！！")
                print('-----')
                continue

            message = f'虎航好康：{travel["departure"]} - {travel["destination"]} {travel["price"]}，旅遊日期：{travel["travel_date"]}，開票日期：{travel["billing_date"]}'
            print(message)
            # line_notify(message, token="xxxxxxxxxx")        # 發送訊息到 line notify，token 要換成自己的
            line_notify(message)        # 發送訊息到 line notify，token 要換成自己的
            message = f'{travel["url"]}'
            print(message)
            line_notify(message)        # 發送訊息到 line notify
            print('-----')

    except Exception as e:
        # 顯示錯誤訊息
        print(f"tiger_air_tw() 出現錯誤: {e}")
        # 顯示錯誤的檔案及錯誤的行數
        print(f"錯誤檔案：{e.__traceback__.tb_frame.f_globals['__file__']} 行數：{e.__traceback__.tb_lineno}")            


