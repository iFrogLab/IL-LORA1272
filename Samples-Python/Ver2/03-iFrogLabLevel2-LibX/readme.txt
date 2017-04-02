


範例1:
二個LoRa 可以做出　gateway　和　Node 的動作資料，
此範例主要是做出啟動時的動作(Ｓtep1) 詳細請看 iLoRa規格書iLoRa_Level_2.txt
ap-gateway-01_init.py
ap-node-01_init.py





* [ ] 啟動時的動作
    * [ ] ​Step 1: 啟動時
    　　　Node 先透過廣播的方法，把自己的4個bytes 的ID對外宣布，透過　default 頻段，發出廣播，並傳出是node 1 還是gateway 0,
    　　　例如:  Node-> broadcast ( LoRaL2_Node_FindGateway ): 0x71, 01, node=0, ID, ActionID=1, CRC,
         成功的話，就會gateway 會透過廣播頻段發回　( LoRaL2_GateWay_FineNode ): 0x72, 01,  gateway=1, 4個bytes Gateway ID, Node Index,  CRC, 為了增加資料長度，所以給一個byte 的Node Index，以後就用這個當成Node 的號碼。
         失敗1. 沒有gateway，就完全沒有消息，1秒後，再發一次。
         失敗2. 已經有這個ID  了，請換另外一個　ID，-> gateway 會透過廣播頻段發回　0x72, ff, 01, gateway=1, 4個bytes Gateway ID,4個bytes 建議Node 的 ID, Freq 3個bytes CRC,
         失敗3. 範圍內有2個 LoRa gateway,會透過廣播頻段發回　0x72, ff,  02, gateway=1, 4個bytes Gateway ID, CRC,
    * [ ] ​Step 2: 啟動初始化
    　　　Node 接著　透過Gateway 給的Node Index和指定的Freq, 送出啟動初始化的確認訊號。
    　　　而ActionID=0 是1對1 加密, 使用特殊Freq
    　　　　　例如:  Node-> 指定的Freq :  0x71, 02, Node Index,  ActionID=1, CRC,
         　　成功的話，就會gateway 會透過廣播頻段發回　0x72, 02,  ActionID=1, gateway Ver, 下一筆添加值, CRC。
    　　　　ActionID=1 是1對1　不加密,  使用特殊Freq(先做　ActionID=1）　
    　　　　　例如:  Node-> 指定的Freq :  0x71, 02, Node Index,  ActionID=1, CRC,
         　　成功的話，就會gateway 會透過廣播頻段發回　0x72, 02,  ActionID=1, gateway Ver,  CRC。
    　　　　ActionID=2 廣播 加密, 使用broadcast　Freq
    　　　　　同　ActionID=0, 使用broadcast　Freq　
    　　　　ActionID=3 廣播 不加密, 使用broadcast　Freq
    　　　　　同　ActionID=1, 使用broadcast　Freq　
    　　　　ActionID=4 是將資料發給另外一個Node不加密, 使用broadcast Freq
    　　　　ActionID=5 Mesh 傳遞,



    　　　　ActionID=6 Mesh 停止傳遞,




* [ ] ​Step 1: 長資料傳遞  ActionID=0,ActionID=1,ActionID=2 ,ActionID=3,
         String Index 的用意是把字串分成數串，並傳遞到Server 後，才組合回來。 　一次只能傳  256次　資料　(255x14-1=3570)
         一次傳 數個 個bytes, Data[0],....
    　　　例如:
          Node-> 指定的Freq       : 第1筆：  0x73,   Node Index, String Index=0, Data[0],....,Data[13].
          gatway 指定的Freq->Node :  成功->  0x72,           03, 回傳 String Index,CRC
          gatway 指定的Freq->Node :  成功(加密版)->  0x72,           03, 回傳 String Index, 下一筆添加值, CRC

          Node-> 指定的Freq       : 第2筆：  0x73,   Node Index, String Index=1,               Data[13+0],....,Data[13+13].
          gatway 指定的Freq->Node :  成功->  0x72,           03, 回傳 String Index,CRC
          gatway 指定的Freq->Node :  成功(加密版)->  0x72,           03, 回傳 String Index,下一筆添加值, CRC

          Node-> 指定的Freq       : 第256筆：  0x73,   Node Index, String Index=255,           Data[(13*255)+0],....,Data[(13*255)+13].
          gatway 指定的Freq->Node :  成功->    0x72,           03, 回傳 String Index,CRC
          gatway 指定的Freq->Node :  成功(加密版)->  0x72,           03, 回傳 String Index,添加值, CRC

          Node-> 指定的Freq       : 最後一筆：  0x74,   Node Index, String Index= 全部資料%255,Data[(13*n)+0],....,Data[(13*n)+13].
          gatway 指定的Freq->Node :  成功->    0x72,           03, 回傳 String Index,CRC







-----protocol spec-------------------------------------------------------------------------------------------------------

1.啟動:
 Node-> broadcast ,       0x71, 01, 0,    Node ID3,   Node ID2,   Node ID1,   Node ID0, CRC
 gatway broadcast->Node   0x72, 01, 1, Gateway ID3,Gateway ID2,Gateway ID1,Gateway ID0, Freq[2], Freq[1], Freq[0], CRC


2. 啟動初始化 :
 Node-> Freq ,            0x71, 02, 0,  Node Index,   ActionID, CRC
 gatway 指定的Freq->Node   0x72, 02, 1,  ActionID, gateway Ver=1,CRC


3. 傳遞長資料 :
Node-> 指定的Freq, 第n筆：  0x73,   Node Index, String Index=n, Data[(13*n)+0],....,Data[(13*n)+13].
gatway 指定的Freq->Node :  成功->  0x72,           03, 回傳 String Index,CRC
Node-> 指定的Freq       : 最後一筆：  0x74,   Node Index, String Index= 全部資料%255,Data[(13*n)+0],....,Data[(13*n)+13].
gatway 指定的Freq->Node :  成功->    0x72,           03, 回傳 String Index,CRC








       gatway 指定的Freq->Node   0x72, 03, 回傳 String Index,CRC
 錯誤， gatway 指定的Freq->Node   0x72, 04, 回傳 String Index,CRC　　//　沒找到，請node 再傳一次　




失敗2. 0x72, ff,  01, gateway=1, 4個bytes Gateway ID, 4個bytes 建議Node 的 ID, Freq 3個bytes CRC,  // 已經有這個ID  了，請換另外一個　ID，-> gateway 會透過廣播頻段發回
失敗3. 0x72, ff,  02, gateway=1, 4個bytes Gateway ID, CRC,  // 範圍內有2個 LoRa gateway,會透過廣播頻段發回　








