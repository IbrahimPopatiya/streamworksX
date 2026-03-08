import os,re
import ffmpeg
from urllib.parse import urlsplit
from pytubefix import YouTube,Playlist
from moviepy.editor import VideoFileClip
from PIL import Image
import pytesseract
from pydub import AudioSegment 
import speech_recognition as sr
import models
import uuid
from sqlalchemy.orm import Session
pytesseract.pytesseract.tesseract_cmd = "C:\Program Files\Tesseract-OCR/tesseract.exe"

def extract_text_from_img(g_image):
    image = Image.open(g_image)
    text = pytesseract.image_to_string(image)
    return text

def download_yt_video(url,username,db):
    
    try:
        yt = YouTube(url)
        max_length = 20
        uuid_filename = str(uuid.uuid4())
        uuuid_filename = f"{uuid_filename}.mp4"
        video_title = yt.title.replace(" ", "_").replace("/", "_").replace("\\", "_") 
        t_filename = re.sub(r'\W+','_',video_title)
        t_filename = t_filename[:max_length]
        file_name = f"{t_filename}.mp4"
        filetype = 'video'
        filextension = os.path.splitext(file_name)[1].replace(".", "")

        print(file_name)

        save_path= f"./data/"
    except:
        print("connection error")

    mp4_streams = yt.streams.get_by_itag(18)

    try:
        mp4_streams.download(output_path=save_path, filename=uuuid_filename)

        print("video download successfully")
    except:
        print("some error")


    file = models.Files(uuidname=uuid_filename,username=username, filename=t_filename,filetype=filetype,filextension=filextension)
    db.add(file)
    db.commit()
    db.refresh(file)    
    return file.uuidname


def download_yt_playlist(playlist_url):
    try:
        p = Playlist(playlist_url)
        for video_url in p.video_urls:
            print(f"downloading video {video_url}")
            download_yt_video(video_url)

        print("all videos has downloaded")    
    except Exception as e:
        print(f"error has occured: {e}")

def download_audio_from_video(audio_url,db):
    try:
        yt = YouTube(audio_url)
        max_length=20
        audio_stream = yt.streams.filter(only_audio=True).first()

        audio_title = yt.title.replace(" ","_").replace("/","_").replace("\\","_")
        a_title = re.sub(r'\W+','_',audio_title)
        a_title = a_title[:max_length]
        audio_filename = f"{a_title}.mp3"
        print(audio_filename)
        audio_path = f"./audio/{audio_filename}"

        os.makedirs(os.path.dirname(audio_path),exist_ok=True)

        audio_stream.download(filename="temp_video.mp4")

        audio = AudioSegment.from_file("temp_video.mp4",format="mp4")
        audio.export(audio_path,format="mp3")

        os.remove("temp_video.mp4")

        print("audio file extracted")

        audio_m = models.Audio(filename=audio_filename)
        db.add(audio_m)
        db.commit()
        db.refresh(audio_m)    
        return audio_m.id

    except Exception as e:
        return f"Error extracting audio: {e}"




def download_audio_from_playlist(audio_playlist_url):
    try:
        p = Playlist(audio_playlist_url)
        for video_url in p.video_urls:
            print(f"downloading audio {video_url}")
            download_audio_from_video(video_url)
        print("all audio has downloaded")
    except Exception as e:
        print(f"error has occured {e}")        



def audio_to_wav(input_file):
    output_file = input_file.replace('.mp3', '.wav')
    # convert mp3 file to wav file 
    sound = AudioSegment.from_mp3(input_file) 
    sound.export(output_file, format="wav") 
    return output_file

def audio_to_text(input_file):
    r = sr.Recognizer()
    audio_file = sr.AudioFile(input_file)
    with audio_file as source:
        audio = r.record(source)
    text = r.recognize_google(audio)  
    print(text)  



def audio_sample(video):
    audio_dir = "./audio/"
    audio_path = os.path.join(audio_dir, "output.mp3")
    try:
        audio = AudioSegment.from_file(video, format="mp4")
        audio.export(audio_path, format="mp3")
        return f"Audio extracted successfully"
    except Exception as e:
        return f"Error extracting audio: {e.stderr.decode()}"


if __name__  == "__main__":
    url = "https://www.youtube.com/watch?v=ACsLvXuaKxw&list=PL8dkiopR1YhLDIVvT5hOS5hXWX5BO52B7&index=1"
    new_url = "https://www.youtube.com/shorts/w3d_-x303ZI"
    f_url = "https://www.youtube.com/watch?v=Nr87whfHUl8"
    # download_audio_from_video(audio_url=f_url)
    playlist_url = "https://www.youtube.com/playlist?list=PL8dkiopR1YhLDIVvT5hOS5hXWX5BO52B7"
    # download_audio_from_playlist(audio_playlist_url=playlist_url)
    # download_yt_playlist(playlist_url=playlist_url)
    # download_yt_video(url=f_url)
    # image_path = "./data/url.png"
    # img_Text = extract_text_from_img(g_image=image_path)
    # print(img_Text)
    # audio_file = "./audio/2-3_min_introduction_video.wav"
    # audio_to_text(input_file=audio_file)
    # video = "./videos/2-3_min_introduction_video.mp4"
    # audio_sample(video=video)
