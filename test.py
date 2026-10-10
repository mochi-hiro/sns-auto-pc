# import os
# import requests
# from dotenv import load_dotenv
# from requests_oauthlib import OAuth1

# load_dotenv()

# x_api_key = os.getenv("X_API_KEY")
# x_api_key_secret = os.getenv("X_API_KEY_SECRET")
# x_access_token = os.getenv("X_ACCESS_TOKEN")
# x_access_token_secret = os.getenv("X_ACCESS_TOKEN_SECRET")

# auth = OAuth1(
#     x_api_key,
#     x_api_key_secret,
#     x_access_token,
#     x_access_token_secret
# )

# response = requests.post(
#     "https://api.x.com/2/tweets",
#     auth=auth,
#     json={
#         "text": "X APIの接続テストです"
#     }
# )

# print(response.status_code)
# print(response.text)

#コマンドプロンプトへのアクセス
#ssh -i "C:\Users\user\Desktop\sns-auto-pc\.ssh\xs174029.key" -p 10022 xs174029@xs174029.xsrv.jp
from datetime import datetime#時間の取得のためにdatetimeをインポート

with open("/home/xs174029/sns-auto/cron_test.txt", "a") as f:#テキストファイルを開く
    f.write(str(datetime.now()) + "\n")#現在の時刻を記述して1行開ける