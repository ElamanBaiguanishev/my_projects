import os
import glob
from pydub import AudioSegment
#
# video_dir = '/home/johndoe/downloaded_videos/'  # Path where the videos are located
# extension_list = ('*.mp4', '*.flv')
#
# os.chdir(video_dir)
# for extension in extension_list:
#     for video in glob.glob(extension):
#         mp3_filename = os.path.splitext(os.path.basename(video))[0] + '.mp3'
#         AudioSegment.from_file(video).export(mp3_filename, format='mp3')

sound = AudioSegment.from_file("1234.mp4").set_channels(1)
sound.export("жестик.wav", format="wav")