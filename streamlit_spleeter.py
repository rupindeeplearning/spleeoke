import pafy
import argparse
import os
import re
import cgi
import ffmpeg
import streamlit as st
import pandas as pd

st.title('Karaoke Generator')

st.header('Enter the URL of the song video here:')
url = st.text_input("YouTube URL of song:","https://www.youtube.com/watch?v=4a5vaIsaxB8")
video = ''
filepath_video = ''
filepath_audio = ''
filepath = 'YoutubeDownload/'
df = pd.DataFrame({
      'first column': [2, 3, 4]
    })
option = st.sidebar.selectbox(
    'Select number of stems',
     df['first column'])

st.header('Number of stems:')
option

if st.sidebar.button('Load & Process Video'):    
    video = pafy.new(url)
    title = "".join(re.findall("[a-zA-Z]+", video.title))
    streams = video.streams 
    for i in streams: 
        print(i) 
          
    # get best resolution of a specific format 
    # set format out of(mp4, webm, flv or 3gp) 
    best = video.getbest(preftype ="mp4") 
    video_name = '{}.{}'.format(title,'mp4')
    print(video_name)
    filepath_video = 'YoutubeDownload/{}.{}'.format(title, best.extension)
    filepath_audio = 'YoutubeDownload/audio.wav'
    os.system('icacls YoutubeDownload /grant Everyone:F /t')    
    
    
    filelist = [ f for f in os.listdir(filepath) if (f.endswith('.wav') or (f.endswith('.mp4')))]
    for f in filelist:
        os.remove(os.path.join(filepath, f))
            
    
    best.download(filepath='/YoutubeDownload/{}.{}'.format(title, best.extension)) 
    os.system('ffmpeg -i ' + filepath_video +' -vn -f wav ' + filepath_audio)
    video_byte = open(filepath_video, 'rb').read()  
    st.subheader('The "Karaoke Video" button will activate when processing is done. Please be patient - the processing takes a few minutes...')    
    st.header('Input Video')    
    st.video(video_byte)
    os.system('ffmpeg -i ' + filepath_video + ' -codec copy -an ' + filepath + 'silent-video.mp4')
    os.system('spleeter separate -i ' + filepath_audio + ' -p spleeter:'+str(2)+'stems -o '+ filepath)  
    os.system('ffmpeg -i ' + filepath + 'silent-video.mp4 -i ' + filepath + '/audio/accompaniment.wav -c:v copy -c:a aac ' + filepath + 'karaoke-video.mp4')
        
    
    
    
    
    

if st.sidebar.button('Karaoke Video'):             
    video_byte = open(filepath + 'karaoke-video.mp4', 'rb').read()  
    st.header('Karaoke Video')
    st.video(video_byte)
