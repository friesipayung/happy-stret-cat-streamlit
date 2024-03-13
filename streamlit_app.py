import pandas as pd
import streamlit as st
from streamlit_player import st_player
import requests
from multiprocessing import Pool

st.set_page_config(
    page_title="Happy Street Cat Data",
    page_icon="🐱",
    layout="wide",
    initial_sidebar_state="expanded",
)


def get_feeders():
    url = "https://api.meow.camera/catHouses/top"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_named_feeder():
    url = "https://api.meow.camera/catHouses/named"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_feeder_data(id):
    url = "https://api.meow.camera/catHouse/{}".format(id)
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_all():
    top_feeders = get_feeders()
    named_feeders = get_named_feeder()

    fs = named_feeders + top_feeders

    # delete duplicate feeders by catHouseId
    fs = [dict(t) for t in {tuple(d.items()) for d in fs}]

    feeder_ids = [f['catHouseId'] for f in fs]
    with Pool(10) as p:
        feeder_data = p.map(get_feeder_data, feeder_ids)
    for i, f in enumerate(fs):
        f['data'] = feeder_data[i]

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
data_df = data_df.sort_values(by='cat', ascending=False)

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
)
