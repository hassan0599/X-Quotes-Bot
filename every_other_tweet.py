from bing_image_downloader import downloader
import main
import json
import os

x = main.make_token()
client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")
token_url = "https://api.twitter.com/2/oauth2/token"

t = main.r.get("token")
bb_t = t.decode("utf8").replace("'", '"')
data = json.loads(bb_t)

refreshed_token = x.refresh_token(
  client_id=client_id,
  client_secret=client_secret,
  token_url=token_url,
  refresh_token=data["refresh_token"],
)

st_refreshed_token = '"{}"'.format(refreshed_token)
j_refreshed_token = json.loads(st_refreshed_token)
main.r.set("token", j_refreshed_token)

content = main.parse_quote()
picture_query = content + " Portrait"
downloader.download(picture_query, limit=1,  output_dir='dataset', adult_filter_off=True, force_replace=False, timeout=60, verbose=True)
media = main.post_image(picture_query)
media = {
  "media_ids": [media]
}
payload = {
  "text": "{}\n- {}".format(content[0], content[1]),
  "media": media
}
main.post_tweet(payload, refreshed_token)
