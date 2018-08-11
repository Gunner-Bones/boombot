import json, urllib.request
UBAUTH = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMTcyODYxNDE2MzY0MTc5NDU2IiwiaWF0IjoxNTMzOTM5MzcyfQ.gDuu8OkXuRbErQ0xQFdssEHLUixKvgUjb8H-GpvLUWQ"
BKSID = "407306176020086784"
GBMID = "172861416364179456"
ubr = urllib.request.Request("https://unbelievable.pizza/api/v1/guilds/" + BKSID + "/users/" + GBMID,headers={'User-Agent':'Mozilla/5.0','Authorization':UBAUTH})
ubr = str((urllib.request.urlopen(ubr).read()))
ubr = json.loads(ubr)
print(ubr)
