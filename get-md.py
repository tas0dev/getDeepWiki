#!/usr/bin/env python3

import os
import requests
import re
import time
import sys

def download_deepwiki_project(base_url):
    base_url = base_url.rstrip('/')
    
    # プロジェクト名の抽出
    project_name = base_url.split('/')[-1]
    if not os.path.exists(project_name):
        os.makedirs(project_name)
        print(f"フォルダ '{project_name}' を作成しました。")

    # メインページを取得して目次を解析
    jina_url = f"https://r.jina.ai/{base_url}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    print(f"目次を取得中: {jina_url}")
    response = requests.get(jina_url, headers=headers)
    
    if response.status_code != 200:
        print(f"エラー: ページの取得に失敗しました。ステータスコード: {response.status_code}")
        return

    pattern = rf'\[.*?\]\(({re.escape(base_url)}/.*?)\)'
    links = re.findall(pattern, response.text)
    
    # 重複削除
    links = list(set(links))
    
    if not links:
        print("ページが見つかりませんでした。URLが正しいか、または目次がMarkdown形式で記述されているか確認してください。")
        return

    print(f"合計 {len(links)} 個のページが見つかりました。")

    for link in links:
        page_id = link.rstrip('/').split('/')[-1]
        file_path = os.path.join(project_name, f"{page_id}.md")

        if os.path.exists(file_path):
            print(f"スキップ: {page_id}")
            continue

        print(f"ダウンロード中: {page_id}...")
        
        page_jina_url = f"https://r.jina.ai/{link}"
        try:
            page_response = requests.get(page_jina_url, headers=headers)
            if page_response.status_code == 200:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(page_response.text)
                print(f"保存完了: {file_path}")
            else:
                print(f"失敗 ({page_response.status_code}): {link}")
            
            time.sleep(0.1) 
            
        except Exception as e:
            print(f"エラー発生 ({link}): {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] in ["-h", "--help"]:
            print("使い方:")
            print("python3 download.py [DeepWikiのURL]")
            print("例: python3 download.py https://deepwiki.com/example/example_project")
            sys.exit(0)
            
        elif sys.argv[1] in ["-v", "--version"]:
            print("DeepWiki Downloader バージョン 1.0")
            sys.exit(0)
            
        elif sys.argv[1] in ["meow", "nya", "nyaa"]:
            print("⠀　　/ヽ　  /ヽ")
            print("　  ‘:’　ﾞ”””　 `’:,　＜ にゃ！")
            print("　 ﾐ　　 ･ω･　 ;,")
            sys.exit(0)
            
        else:
            url = sys.argv[1]
            download_deepwiki_project(url)
    else:
        print("使い方:")
        print("python3 download.py [DeepWikiのURL]")
        print("python3 download.py https://deepwiki.com/example/example_project")