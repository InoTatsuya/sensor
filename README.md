# sensor
raspberry piとGWとしたセンサデータのロギング基盤  
対応センサは以下(チャージコントローラはセンサではないがロギングしたいのでしょうがない)
- twelite無線タグアプリ：SHT-30,SEN0193

# 物理構成
エッジ側：twelite子機 - twelite親機(MONOSTICK) - raspberry pi  
サーバ側：aws ec2 ubuntu + mysql

# ファイル構成
## ./edge(エッジ側)
├── dataPostTwelite.py：tweliteログの受信/解析/POST送信  
├── param_edge_dummy.py：ログ受信用USBポートや送信先サーバの定義など  
└── param_edge.py：上記を設定してリネームしたもの  

## ./server(サーバ側)
├── createTbl.sql：mysqlセンサテーブルの定義  
├── dash_twelite.py：python-dashを使用したデータ可視化webサーバを立てる  
├── dataReceiveTwelite.py：センサデータ(twelite,チャージコントローラ)を受信/解析/保存(mysql)  
├── initial.sql：mysqlにデータベースとユーザーを作るやつ  
├── param_server_dummy.py：センサデータ受信用のポートとかwebサーバ用の定義とか  
├── param_server.py：上記を設定してリネームしたもの  
└── sensor_db.sql：mysqlのデータベース情報のバックアップ、いらんからそのうち消す  
