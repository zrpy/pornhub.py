import requests
from tqdm import tqdm

def download_path(f,u,i,bar):
        r = requests.get(u.split("master")[0]+i)
        for chunk in r.iter_content(chunk_size=1024):
            f.write(chunk)
            if bar:
                bar.update(1)

def get_info(view_key):
    u = requests.get("https://jp.pornhub.com/view_video.php?viewkey={}".format(view_key)).text.split('"format":"hls","videoUrl":"')[1].split('"')[0].replace("\\","")
    v = [i for i in requests.get(u.split("master")[0]+[i for i in requests.get(u).text.splitlines() if "?" in i][0]).text.splitlines() if "?" in i]
    return u,v


def download(path:str,view_key:str,log:bool=True):
    url,videos=get_info(view_key)
    if log:
        bar = tqdm(
            desc="Downloading",
            total=len(videos),
            unit='B',
            unit_scale=True,
            unit_divisor=2048,
            leave=True,
            position=0
        )
    else:
        bar = None
    with open("{}.mp4".format(path),"wb") as f:
        for i in videos:
            download_path(f,url,i,bar)

