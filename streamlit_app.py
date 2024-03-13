import streamlit as st
import ffmpeg
from streamlit_player import st_player

url = "https://streetcatpull.hellobike.com/live/4754408094082753545_0.m3u8"
st_player(url, playing=True, loop=True, controls=True, volume=0.5)
st.text(url)


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