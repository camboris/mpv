"""Main module."""
import requests
import logging
import json
from datetime import datetime, timedelta
from slugify import slugify

# logging.basicConfig(filename='mpv.log', encoding='utf-8', level=logging.DEBUG)
logger = logging.getLogger("mpv")

queries = [
    {
        'id': 'depto',
        'url': 'https://api.maspocovendo.com/api/publications/search?category=MLA1473&cities=Rafaela,+Santa+Fe&lat=-31.24552&lon=-61.49147&distance=250&page=1&per_page=50'
    },
    {
        'id': 'casa',
        'url': 'https://api.maspocovendo.com/api/publications/search?category=MLA1467&cities=Rafaela,+Santa+Fe&lat=-31.24552&lon=-61.49147&distance=250&page=1&per_page=50'
    }
]

wh = "https://discord.com/api/webhooks/824831189981593600/084mhOQiVl19aUnJ4DEkmLJD9z1uKMlcC7sfczR1g1V94TbO-pAtOVVMcp2ZHOizHicw"

mpv_base_url = "https://www.maspocovendo.com/{}/{}"
maps_base_url = "https://www.google.com/maps/@{},{},18z"
# mpv_date_now = datetime.now()

def procesar_query(query, last):
    items = []

    last_date = datetime.strptime(last['last_date'], '%Y-%m-%d %H:%M:%S')
    id = query['id']
    url = query['url']

    r = requests.get(url);

    data = r.json()
    posts = data['data']

    for post in posts:
        # innecesario, toma cualquier cosa antes del id
        post_date = datetime.strptime(post['date'], '%Y-%m-%d %H:%M:%S')

        if post_date > last_date:
            items.append(post)

    return items


def notificar_items(items, query):
    for item in items:
        post_slug = slugify(item['title'])
        post_id = item['id']
        post_url = mpv_base_url.format(post_slug, post_id)

        discord = {
            "content": query["id"],
            "embeds": [{
                "title": item['title'],
                "url": post_url,
                "fields": [{
                    "name": "Alquiler",
                    "value": item['price'],
                    "inline": True
                },{
                    "name": "Fecha",
                    "value": item['date'],
                    "inline": True
                },{
                    "name": "Ubicacion",
                    "value": maps_base_url.format(item["geopoint"]["coordinates"]["latitude"],item["geopoint"]["coordinates"]["longitude"] ),
                    "inline": False
                }]
                # "image": {
                #     "url": item["media"][0]["image_file_name"]
                # }
            }]
        }
        # djson = json.dumps(discord, default=str)
        p = requests.post(wh, json=discord)
        # print(djson)
        print(p.status_code)


def save_last_item(items):
    if len(items) == 0:
        return

    last_item = {
        "last_date": datetime.strptime(items[0]['date'], '%Y-%m-%d %H:%M:%S'),
        "last_id": items[0]['id']
    }

    for item in items:
        item_date = datetime.strptime(item['date'], '%Y-%m-%d %H:%M:%S')
        if item_date > last_item['last_date']:
            last_item = {
                "last_date": item_date,
                "last_id": item['id']
            }

    return last_item


def open_last():
    with open('output/mpv_last.json', 'r') as infile:
        data = json.load(infile)

    return data


def save_last(last_dict):
    with open('output/mpv_last.json', 'w') as outfile:
        # json.dumps(last_json, default=str))
        json.dump(last_dict, outfile, default=str)


if __name__ == "__main__":
    # mpv_base_date = datetime.now() - timedelta(hours=1)
    # mpv_base_date = datetime.strptime('2021-03-19 11:54:02', '%Y-%m-%d %H:%M:%S')
    # logger.info(mpv_base_date)
    last_dict = open_last()
    for q in queries:
        items = procesar_query(q, last_dict[q['id']])
        notificar_items(items, q)
        last_item = save_last_item(items)

        if last_item is not None:
            last_dict[q['id']] = last_item

    save_last(last_dict)
