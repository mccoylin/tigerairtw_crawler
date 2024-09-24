# tigerairtw_crawler

取得台灣虎航「特別優惠」的資料，並傳送到 line notify。

    環境 : python 3

    採用 requests.get() 取得網頁資料
    採用 re 拆解並組合網頁資料
    透過 line notify API 發送訊息
