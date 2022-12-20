import requests
import os
import datetime
import csv
import time
import configparser


config_ini = configparser.ConfigParser()
config_ini.read('config.ini', encoding="utf-8")

if config_ini.get("USER_SETTING", "use_proxy") == "yes":
    os.environ["HTTP_PROXY"] = config_ini.get("USER_SETTING", "proxy_url")
    os.environ["HTTPS_PROXY"] = config_ini.get("USER_SETTING", "proxy_url")
API_KEY = config_ini.get("USER_SETTING", "deepl_api_kay")
API_URL = config_ini.get("USER_SETTING", "deepl_api_url")


def csv_log(source_text, target_text, target_lang, time):
    if config_ini.get("USER_SETTING", "log_csv_path") == "None":
        path = "log.csv"
    else:
        path = os.path.join(config_ini.get(
            "USER_SETTING", "log_csv_path"), 'log.csv')
    with open(path, mode='a', newline="\n", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.datetime.now(), target_lang,
                        len(source_text), time, source_text, target_text])


def translate(source_text, target_langage, split_sentences):
    # URLクエリに仕込むパラメータの辞書を作っておく
    if target_langage == "JA":
        params = {
            "auth_key": API_KEY,
            "text": source_text,
            "source_lang": 'EN',  # 入力テキストの言語を英語に設定
            "target_lang": 'JA',  # 出力テキストの言語を日本語に設定（JPではなくJAなので注意）
            "preserve_formatting": "0"
        }
    else:
        params = {
            "auth_key": API_KEY,
            "text": source_text,
            "source_lang": 'JA',  # 入力テキストの言語を英語に設定
            "target_lang": 'EN',  # 出力テキストの言語を日本語に設定（JPではなくJAなので注意）
            "preserve_formatting": "0"
        }
    if split_sentences == 1:
        params["split_sentences"] = "nonewlines"
    else:
        params["split_sentences"] = "1"
    start_time = time.time()
    try:
        # パラメータと一緒にPOSTする
        # free用のURL、有料版はURLが異なります
        request = requests.post(f"https://{API_URL}/v2/translate", data=params)
        request.raise_for_status()
        result = request.json()
        elapsed_time = time.time()-start_time
        target_text = result["translations"][0]["text"]
        csv_log(source_text, target_text, target_langage,
                round(elapsed_time, 5))
    except requests.exceptions.RequestException as e:
        target_text = "Error:" + str(e)

    return target_text


def usage_request():
    usage_request = requests.post(
        f"https://{API_URL}/v2/usage", data={"auth_key": API_KEY}
    )
    usage_request.raise_for_status()
    usage_result = usage_request.json()
    usage_result = {
        "character_count": usage_result["character_count"],
        "character_limit": usage_result["character_limit"]}
    return usage_result
