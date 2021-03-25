"""Main module."""
import requests
from datetime import datetime, timedelta
from slugify import slugify

queries = [
    {
        'id': 'depto',
        'url': 'https://api.maspocovendo.com/api/publications/search?category=MLA1473&cities=Rafaela,+Santa+Fe&lat=-31.24552&lon=-61.49147&distance=250&page=1&per_page=50'
    },
    {
        'id': 'casas',
        'url': 'https://api.maspocovendo.com/api/publications/search?category=MLA1467&cities=Rafaela,+Santa+Fe&lat=-31.24552&lon=-61.49147&distance=250&page=1&per_page=50'
    }
]

mpv_base_url = "https://www.maspocovendo.com/{}/{}"
mpv_date_now = datetime.now()

def procesar_query(query):
    id = query['id']
    url = query['url']

    r = requests.get(url);

    data = r.json()
    posts = data['data']

    for post in posts:
        # https://www.maspocovendo.com/se-alquila-departamento-excelente-con-cochera/26750
        # print("{} - {}".format(post['id'], post['title']))
        # print("{}".format(slugify(post['title'])))
        post_slug = slugify(post['title'])
        post_id = post['id']
        post_date = datetime.strptime(post['date'], '%Y-%m-%d %H:%M:%S')

        if post_date > mpv_base_date:
            print(post_date)
            print(mpv_base_url.format(post_slug, post_id))


if __name__ == "__main__":
    mpv_base_date = datetime.now() - timedelta(hours=1)
    mpv_base_date = datetime.strptime('2021-03-19 11:54:02', '%Y-%m-%d %H:%M:%S')
    print(mpv_base_date)
    for q in queries:
        print(q['id'])
        procesar_query(q)
