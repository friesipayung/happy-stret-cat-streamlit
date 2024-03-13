import os

import pandas as pd
import streamlit as st
import requests
from multiprocessing import Pool
import redis

st.set_page_config(
    page_title="Happy Street Cat Data",
    page_icon="🐱",
    layout="wide",
    initial_sidebar_state="expanded",
)

r = redis.Redis(
    host=os.environ.get('REDIS_HOST', 'localhost'),
    port=os.environ.get('REDIS_PORT', 6379),
    password=os.environ.get('REDIS_PASSWORD', None),
    ssl=True
)

ttl = os.environ.get('REDIS_TTL', 60*2)


def get_feeders():
    url = "https://api.meow.camera/catHouses/top"
    response = requests.get(url, timeout=30)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_named_feeder():
    url = "https://api.meow.camera/catHouses/named"
    response = requests.get(url, timeout=30)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def check_redis(id):
    d = r.get(id)
    if d:
        return d.decode('utf-8')
    else:
        return None


def save(id, d):
    r.set(id, str(d))
    r.expire(id, ttl)  # 30 seconds expire time


def get_feeder_data(id):
    d = check_redis(id)
    if d:
        return d

    url = "https://api.meow.camera/catHouse/{}".format(id)
    response = requests.get(url, timeout=30)
    if response.status_code == 200:
        d = response.json()
        d['catHouseId'] = id
        save(id, d)
        return d
    else:
        return {}


def get_all():
    top_feeders = get_feeders()
    named_feeders = get_named_feeder()

    fs = named_feeders + top_feeders

    # delete duplicate feeders by catHouseId
    fs = [dict(t) for t in {tuple(d.items()) for d in fs}]

    feeder_ids = [f['catHouseId'] for f in fs]

    with Pool(4) as p:
        for result in p.imap(get_feeder_data, feeder_ids):
            print("result = ", result)
            for i, f in enumerate(fs):
                if f['catHouseId'] == result['catHouseId']:
                    f['data'] = result

    return fs


feeders = get_all()

datas = []
for feeder in feeders:
    feeder_id = feeder.get('catHouseId', 0)
    name = feeder.get('englishName', None)
    if name is None:
        name = feeder.get('data', {}).get('englishName', None)
    data = {
        "feeder_id": feeder_id,
        "url": "https://meow.camera/viewer/#{}".format(feeder_id),
        "name": name,
        "original_name": feeder.get('name', '-'),
        "cat": feeder.get('data', {}).get('catPresent', False),
        "snack": feeder.get('data', {}).get('hasSnacks', False),
    }
    datas.append(data)

data_df = pd.DataFrame(datas)

# sort by cat presence
data_df = data_df.sort_values(by='name', ascending=False)

st.data_editor(
    data_df,
    column_config={
        "url": st.column_config.LinkColumn(
            "URL", display_text="Open video url"
        ),
    },
    hide_index=True,
    column_order=["name", "original_name", "cat", "snack", "url", "feeder_id"],
    use_container_width=True,
    height=800,
)
