import streamlit as st
from streamlit_player import st_player

DEFAULT_FEEDER = "4754408094082753545"

params = st.query_params.to_dict()
feeder_id = params.get('feeder')


if feeder_id is None:
    feeder_id = DEFAULT_FEEDER

url_base = "https://streetcatpull.hellobike.com/live/{}_{}.m3u8"

for i in range(3):
    url = url_base.format(feeder_id, i)
    st_player(url, height=250, playing=True, light=True, controls=True, volume=1,  playback_rate=1, progress_interval=100)
    st.markdown("[{}]({})".format(url, url))

# input = ffmpeg.input(url)
# audio = input.audio.filter("aecho", 0.8, 0.9, 1000, 0.3)
# video = input.video.hflip()
# out = ffmpeg.output(audio, video, 'pipe')
# out.run_async()


#
# process1 = (
#     ffmpeg
#     .input(url)
#     .output('pipe:', format='ismv', vcodec='copy')
#     .run_async(pipe_stdout=True)
# )
#
# while True:
#     in_bytes = process1.stdout.read(32768)
#     if not in_bytes:
#         break
#
#     st.write(in_bytes)
#

# process1.wait()