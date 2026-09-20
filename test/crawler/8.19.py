#3.3.3 爬取音频
import time
import requests
from lxml import etree
"""
url="https://mp.weixin.qq.com/s/JHioeDcopm-98R5lGVemqw"
audio_url="https://res.wx.qq.com/voice/getvoice"
headers = {
    'Host': 'mp.weixin.qq.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}
response=requests.get(url,headers=headers)
print(response)
resp=requests.get(url,headers=headers).text

html=etree.HTML(resp)
print(html)
save_path=r"E:/savepath/audio/"
def download_audio(fileid,title):
    try:
        audio_content=requests.get(audio_url,params={"mediaid":fileid,"voice_type":1})
        if audio_content is not None:
            audio_name=title+str(int(time.time()))+".mp3"
            print("download:",audio_name,"url:",audio_content.url)
            with open(save_path+audio_name,"wb+")as f:
                f.write(audio_content.content)
                print("audio download finished.:",audio_name)
        else:
            print("空空如也")
    except Exception as reason:
        print(str(reason))
def get_audio_id(c):
    audios=c.xpath("//mpvoice/@voice_encode_fileid")
    titles=c.xpath("//mpvoice/@name")
    print(audios)
    print(titles)
    for audio in audios:
        download_audio(audio,titles[0])
get_audio_id(html)
"""

url="https://v.qq.com/x/cover/mzc00200aaogpgh/r0047gdjpw6.html?scene_id=3"
headers={
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}
resp=requests.get(url,headers=headers)
print(resp.text)
