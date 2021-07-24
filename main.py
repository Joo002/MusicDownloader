from youtubesearchpython import VideosSearch
import youtube_dl
import os
from pydub import AudioSegment


filter_neg = {"loop", "hour", "cover", "official video", "mv","m/v" , "뮤직비디오", "acoustic", "어쿠스틱", "ver", "fan", "1시간", "연속 재생", "반복 재생", "연속재생", "반복재생"}
filter_pos = {
    "lyrics": 5,
    "가사": 5
}


#title = input("title? ")
#artist = input("artist? ")
#duration = int(input("duration? "))
title = "되돌리다"
artist = "이승기"
duration = 265
title_ = title.replace(" ", "+")
artist_ = artist.replace(" ", "+")

result = VideosSearch(f"{artist_} {title_} 가사", limit = 10).result()

#title__ = title.replace(" ", "%20")
#artist__ = aritst.replace(" ", "%20")
#requests.request f"https://music.bugs.co.kr/search/integrated?q={title__}%20{artist__}"


mosts = {}


for i in result["result"]:
    score = 0
    result_title = i["title"].lower()
    result_artist = i["channel"]["name"].lower()
    result_duration = (int(i['duration'].split(":")[0]) * 60) + int(i['duration'].split(":")[1])
    for j in filter_neg:
        if j in result_title:
            score = -1
            break

    if score != -1:
        score = abs(result_duration - duration)
        if score < 2:
            score = 0
        score += 10

    for j in filter_pos:
        if j in result_title:
            score -= 5
            break

    if score != -1:
        mosts[i["link"]] = score
    
    print(("\033[31m" if score == -1 else "\033[0m") + f"[{score}]\t{result_title}  |  {result_artist}  |  {result_duration}" "\033[0m")
    
mosts = sorted(mosts.items(), key=lambda mosts: mosts[1])
for i in mosts:
    print(i[0])



ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '320',
    }],
}
url = mosts[0][0]
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])