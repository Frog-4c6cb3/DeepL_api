import requests
import os
import datetime
import csv
import time

# os.environ["HTTP_PROXY"] = "http://10.9.210.229:8080"
# os.environ["HTTPS_PROXY"] = "http://10.9.210.229:8080"
API_KEY = "b5e03c0f-1fbd-97fa-a0e8-3f59d37b7ca6:fx"


def csv_log(source_text, target_text, target_lang, time):
    path = os.path.join(os.path.dirname(__file__), 'log.csv')
    with open(path, 'a', newline="") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.datetime.now(), target_lang,
                        len(source_text), time, source_text, target_text])


def translate(source_text, target_langage):
    # URLクエリに仕込むパラメータの辞書を作っておく
    if target_langage == "JA":
        params = {
            "auth_key": API_KEY,
            "text": source_text,
            "source_lang": 'EN',  # 入力テキストの言語を英語に設定
            "target_lang": 'JA'  # 出力テキストの言語を日本語に設定（JPではなくJAなので注意）
        }
    else:
        params = {
            "auth_key": API_KEY,
            "text": source_text,
            "source_lang": 'JA',  # 入力テキストの言語を英語に設定
            "target_lang": 'EN'  # 出力テキストの言語を日本語に設定（JPではなくJAなので注意）
        }
    start_time = time.time()
    try:
        # パラメータと一緒にPOSTする
        # free用のURL、有料版はURLが異なります
        request = requests.post(
            "https://api-free.deepl.com/v2/translate", data=params)
        request.raise_for_status()
        result = request.json()
        elapsed_time = time.time()-start_time
        target_text = result["translations"][0]["text"]
        csv_log(source_text, target_text, target_langage, round(elapsed_time, 5))
    except requests.exceptions.RequestException as e:
        target_text="Error:" + str(e)

    return target_text
