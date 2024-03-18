from base64 import b64decode
from requests import get
from json import loads
from re import search
from time import monotonic

print('cdn_ID. ie. "?v=VswFqVUmq" without "?v=". Note: ID should be 9 characters')
cdn_ID = input("Enter cdn_ID: ") 

# leave empty for 360p
# add "www" for 720p
# add "whw" for 1080p
# if 1080p is not available, it will use the next highest quality
q_prefix = "whw"

domain, vid_id, sources = \
    [loads(b64decode(search(r'PLAYER\(atob\("(.*?)"', get(f"https://abysscdn.com/?v={cdn_ID}").text).group(1)))[i] for i in ["domain", "id", "sources"]]

print(f"""
360p  =  " "  = "sd", "mHd"
720p  = "www" = "hd"
1080p = "whw" = "fullHd"

Available sources {sources}
Downloading "{q_prefix}" or next highest source available
Please wait...
""")

get_url = f"https://{domain}/{q_prefix}{vid_id}"
print(get_url)

response = get(f"https://{domain}/{q_prefix}{vid_id}", headers={"Referer": f"https://abysscdn.com/?v={cdn_ID}"}, stream=True)
file_size = int(response.headers['content-length'])
downloaded = 0
start = last_print = monotonic()

with open(f"{cdn_ID}.mp4", "wb") as f:
    for chunk in response.iter_content(chunk_size=8192):
        downloaded += f.write(chunk)
        now = monotonic()
        if now - last_print > 1:
            pct_done = round(downloaded / file_size * 100)
            speed = round(downloaded / (now - start) / 1024)
            print(f'Download {pct_done:{3.0}f}% done | {speed:{5.0}f} Kbps | {speed/100:{6.2}f} Mbps')
            last_print = now
