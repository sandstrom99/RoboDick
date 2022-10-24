import asyncio
import scathach
import requests
scathach.ass()

tags = {
    "gif": "/gif",
    "ass": ""
}

res = requests.get("https://scathach.redsplit.org/v3/nsfw/gif")
json = res.json()
print(json["url"])
