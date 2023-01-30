#################################
#transcript.ipynbの内容をまとめる
#################################

import csv
import os
import tqdm
import youtube_dl
import whisper
model = whisper.load_model("large")

#################################
##########title, urlを受け取りmp3ファイルを保存する
#################################

def downloadmp3(title, url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl':  title + '.%(ext)s',
        'postprocessors': [
            {'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
             'preferredquality': '192'},
            {'key': 'FFmpegMetadata'},
        ],
    }

    ydl = youtube_dl.YoutubeDL(ydl_opts)
    info_dict = ydl.extract_info(url, download=True)

#################################
##########csvからURLとタイトルを取得
#exp>
#('＃０５【 ドラクエIV 】第五章、いざキングレオ！！目指せ瞬殺【雪花ラミィ/ホロライブ】※ネタバレあり','https://www.youtube.com/watch?v=mtI6kTzjEyQ')
#################################

#(タイトル, URL)のタプルの配列が配信者の名前がキーとなった辞書
TitleURLs = {}

for files in os.listdir("./csv"):
    tmp = []
    print(files)
    with open("./csv/" + files) as f:
        reader = csv.reader(f)
        for row in reader:
            tmp.append((row[1], row[3]))
            
    name = files.split("_")[2]
    TitleURLs[name] = tmp
    
#配信者リスト
vtuberlist = list(TitleURLs.keys())

#################################
##########配信ごとに，文字起こしを行う．
#################################

for vtuber in tqdm.tqdm(vtuberlist):
    URLsTitles[vtuber].pop(0)#headerを除去
    for item in tqdm.tqdm(URLsTitles[vtuber], leave=False):
        title = item[0]
        url = item[1]
        
        downloadmp3(title, url)#title,urlを渡し，音声ファイルをダウンロード
        
        #文字起こし
        result = model.transcribe("./" + title + ".mp3", verbose=False, fp16=True, language="ja")
        
        #保存
        with open("./transcription/" + title + ".txt", "w") as f:
            f.write(result["text"])
            
        #音声ファイルを削除
        os.remove("./" + title + ".mp3")