from openai import OpenAI #openai library import
from dotenv import load_dotenv #dotenv library import
import os #os library import
import datetime #現在の時間の取得のためにdatetimeをインポート
import gspread
from google.oauth2.service_account import Credentials
import requests
from requests_oauthlib import OAuth1
#Google  cloudの認証情報を使用してGoogle Sheetsにアクセスするための設定
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets", #google sheetsのファイルにアクセスするためのスコープを追加
    "https://www.googleapis.com/auth/drive" #google driveのファイルにアクセスするためのスコープを追加
]
credentials = Credentials.from_service_account_file("sns-automation-509206-59ddced6804c.json",scopes=SCOPES)
sheets_client = gspread.authorize(credentials)
sheets = sheets_client.open("SNS自動投稿") #Google Sheetsの指定
sheet = sheets.worksheet("投稿データ") #Google Sheetsの指定
result_sheet = sheets.worksheet("result") #Google Sheetsの指定
#googleからデータを取得する
try:
    data = sheet.get_all_records()
except Exception as e:
    print("Google Sheetsのデータ取得エラー:", e)
    exit()
#openaiのAPIキーを環境変数から取得するためにdotenvを使用
load_dotenv() #.envを読み込む
#.envからopenAiキーの取得
api_key = os.getenv("OPENAI_API_KEY") #環境変数から値を取り出す
openAi_client = OpenAI(api_key=api_key) #openai client initialization
api_key = os.getenv("OPENAI_API_KEY") #環境変数から値を取り出す
#.envからXのキー取得
x_api_key = os.getenv("X_API_KEY")
x_api_key_secret = os.getenv("X_API_KEY_SECRET")
x_access_token = os.getenv("X_ACCESS_TOKEN")
x_access_token_secret = os.getenv("X_ACCESS_TOKEN_SECRET")
#XのAPIキーを作成
x_api_key = os.getenv("X_API_KEY")
x_api_key_secret = os.getenv("X_API_KEY_SECRET")
x_access_token = os.getenv("X_ACCESS_TOKEN")
x_access_token_secret = os.getenv("X_ACCESS_TOKEN_SECRET")
#各種Xキーの格納
auth = OAuth1(
    x_api_key,
    x_api_key_secret,
    x_access_token,
    x_access_token_secret
)

for row_number, row in enumerate(data, start=2):#rowでデータを一行ずつ取得 i<row<enumerate()data
    if row["状態"] =="未":
        post_materials = row["投稿ネタ"]
        post_supplement = row["補足"]
        post_id = row["ID"]
        post_date = row["投稿日"]
        sheet.update_cell(row_number, 5, "済") #状態を「済」に更新
        break
if post_materials is None:#データに[未]がなかった場合([未]だった場合post_materialsにデータが格納されないため)
    print("投稿データがありません")
    exit()

#opeaiのAPIを使用してSNS投稿の返信を生成する
try:
    responses = openAi_client.responses.create(
        model="gpt-4o-mini",
        instructions="""
            あなたはSNS投稿作成アシスタントです。
            ・親しみやすい
            ・初心者にも分かりやすい
            ・押し付けない
            ・X向けに読みやすくする
            ・必要に応じて絵文字を使う
        """,
        input=f"""
                投稿ネタ：
                {post_materials}

                補足：
                {post_supplement}
                上記の投稿ネタと補足をもとに、SNS投稿用の文章を作成してください。
                【投稿ルール】
                ・120文字程度で作成してください
                ・140文字を超えないでください
                ・読みやすい文章にする
                ・初心者にも分かりやすくする
                ・ハッシュタグを適切に含める
            """,
    )
except Exception as e:
    print("OpenAI APIエラー:", e)
    exit()
#文字数制限の確認
post_text = responses.output_text
post_length = len(post_text)
if post_length > 140:
    post_result = "文字数超過"

else:
    try:
        #xに接続して
        response = requests.post(
            "https://api.x.com/2/tweets",
            auth=auth,
            json={
                "text": post_text#googleから取得された投稿データをxへ
            }
        )
    except Exception as e:
        print("Xへの通信エラー:", e)
    if response.status_code ==201:
        post_result= "投稿成功"
        status_code = response.status_code
        status_text = response.text
    else:
        post_result = "投稿エラー"
        print("Xエラー:", response.status_code)
        status_code = response.status_code
        print(response.text)
        status_text = response.text


#resultシートの一番下に追加
try:
    result_sheet.append_row([
        post_id,
        post_date,
        post_text,
        post_length,
        post_result,
        status_code,
        status_text
    ])
except Exception as e:
    print("Resultシートへのデータ追加エラー:", e)
    exit()

print("結果:", post_result)

#まとめてコメントアウトしたい場合には、別のショートカットを使用する。 それは、「ctr+/

#post_resultの中身
# ① 140字超過 → "投稿文字数エラー"
# ② X投稿失敗 → "投稿エラー"
# ③ X投稿成功 → "投稿済" 