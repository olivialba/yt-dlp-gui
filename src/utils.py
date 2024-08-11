import dearpygui.dearpygui as dpg
import yt_dlp, requests, io, os
from PIL import Image
import numpy as np
import tkinter as tk
from tkinter import filedialog

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'


class Logs():
    INVALID = 'Video link invalido!'
    SEARCHING = 'Stiamo cercando il video.. Aspetta...'
    FOUND = 'Video trovato!'
    DOWNLOADING = 'Stiamo scaricando il tuo video..'
    DOWNLOAD_FINISHED = 'Video scaricato!'


####### GUI #######

def setLog(text: str):
    dpg.set_value('request_response', addEmptySpaceToText(text))

def getLog():
    return dpg.get_value('request_response')

def addEmptySpaceToText(text: str):
    length = len(text)
    spaces = " " * (75 - length)
    return spaces + text

# Add space in GUI
def space(height: int):
    dpg.add_spacer(height=height)


####### REQUEST #######

# Send Request
def send_request():
    request_url = dpg.get_value('request_url').strip()
    if not request_url.startswith('http'): 
        setLog(Logs.INVALID)
        return None
    
    try:
        dpg.disable_item('send_request_button')
        setLog(Logs.SEARCHING)
        resetInfo()

        info = getVideoInfos(request_url)
        
        # Video Title
        dpg.show_item('request_title')
        dpg.set_value('request_title', f"Title: {info['title']}")
        # Video Author
        dpg.show_item('request_author')
        dpg.set_value('request_author', f"Author: {info['uploader']}")
        # Video Length
        dpg.show_item('request_length')
        dpg.set_value('request_length', f"Duration: {info['duration_string']}")
        # Video Thumbnail
        dpg.show_item('request_quality_title')
        dpg.show_item('request_quality')
        display_thumbnail(info['thumbnail'])
        # Video Quality
        qualities = ['Recommended Quality']
        formats = info.get('formats', [info])
        for f in formats:
            if f['ext'] == "mp4":
                res = (f['resolution']).rsplit('x', 1)
                # 'format_id' for resolution id
                if len(res) == 2 and res[1].isdigit():
                    if res[1] not in qualities:
                        qualities.append(res[1])
        dpg.configure_item('request_quality', items=qualities, default_value='Recommended Quality')
        # Link Url
        dpg.set_value('request_url_info', info['webpage_url'])
        # Download Button
        dpg.show_item('request_download_video')
        # Video Trovato
        setLog(Logs.FOUND)
        
    except Exception as e:
        setLog("Errore: Il link che hai dato non corrisponde a nessun video. Errore nel recupero delle informazioni.")
        print(e)
        return None
    finally:
        dpg.enable_item('send_request_button')
        
def getVideoInfos(URL):
    """
    Checks if the url link corresponds to a video.
    """
    ydl_opts = {
        'quiet': True,
        'noplaylist': True,
        'no_warnings': True,
        }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(URL, download=False)
    return info
    
def resize_zoom(image, width, height):
    # Calculate new dimensions after zooming
    new_width, new_height = image.size
    aspect_ratio = new_width / new_height
    
    # Resize the image
    if width and height:
        if width / aspect_ratio < height:
            new_width = width
            new_height = int(width / aspect_ratio)
        else:
            new_width = int(height * aspect_ratio)
            new_height = height

        image = image.resize((new_width, new_height))
    elif width:
        new_width = width
        new_height = int(width / aspect_ratio)
        image = image.resize((new_width, new_height))
    elif height:
        new_height = height
        new_width = int(height * aspect_ratio)
        image = image.resize((new_width, new_height), resample=2)
    return new_width, new_height, image

def display_thumbnail(thumbnail_url):
    response = requests.get(thumbnail_url)
    image_data = response.content
    
    image = Image.open(io.BytesIO(image_data))
    image = image.convert("RGBA")
    image_width, image_height, image = resize_zoom(image, width=410, height=None)
    image_data = np.frombuffer(image.tobytes(), dtype=np.uint8) / 255.0
        
    with dpg.texture_registry():
        dpg.add_static_texture(image_width, image_height, image_data, tag="request_thumbnail")
    dpg.add_image(texture_tag="request_thumbnail", tag='request_thumbnail_item', before='request_quality_group')
    
def resetInfo():
    dpg.hide_item('request_title')
    dpg.set_value('request_length', "")
    dpg.set_value('request_author', "")
    dpg.hide_item('request_download_video')
    dpg.set_value('request_url_info', "")
    dpg.hide_item('request_quality_title')
    dpg.hide_item('request_quality')
    download_info(turn_on=False)
    
    exists = dpg.does_item_exist('request_thumbnail')
    if exists:
        dpg.delete_item('request_thumbnail')
        dpg.delete_item('request_thumbnail_item')

def downloadVideo():
    if getLog() == Logs.DOWNLOADING:
        print("Video has not finished downloading!")
    dpg.disable_item('request_download_video')
    dpg.disable_item('send_request_button')
    root = tk.Tk()
    root.withdraw()
    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    file_path = filedialog.asksaveasfilename(defaultextension=".mp4",
                                             initialdir=desktop_path,
                                             filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")])
    root.destroy()
    if file_path is None or file_path == "":
        return None
    file_destination = os.path.splitext(file_path)[0]
    
    if not dpg.does_item_exist('request_quality'):
        return None
    res = dpg.get_value('request_quality')
    if res == 'Recommended Quality':
        format_res = f"bestvideo*[ext=mp4]+bestaudio/best"
    else:
        format_res = f"bestvideo*[ext=mp4][height<={res}]+bestaudio/best"
        
    ydl_opts = {
        'outtmpl': file_destination + ".%(ext)s",
        'format': format_res,
        "noplaylist": True,
        'concurrent_fragment_downloads': 4,
        'progress_hooks': [progress_hook],
        }
    #no_warnings
    #quiet
    print(f"File downloading at '{file_destination}'")
    setLog(Logs.DOWNLOADING)
    download_info(turn_on=True)
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([dpg.get_value('request_url_info')])
    dpg.enable_item('request_download_video')
    dpg.enable_item('send_request_button')

def progress_hook(data):
    if data['status'] == 'finished':
        setLog(Logs.DOWNLOAD_FINISHED)
    elif data['status'] == 'downloading':
        total_bytes = data.get('total_bytes', data.get('total_bytes_estimate'))
        percentage = (data['downloaded_bytes'] / total_bytes) * 100
        dpg.set_value('request_download_progress', f"Download Percentage: {percentage:.2f}%")

        speed_mbps = data.get('speed', 1) / (1024 * 1024)
        dpg.set_value('request_download_speed', f"Download Speed: {speed_mbps:.2f} MB/s")
        
        elapsed_minutes = data.get('elapsed', 1) / 60
        dpg.set_value('request_download_elapsed', f"Time Elapsed: {elapsed_minutes:.2f} minutes")

def download_info(turn_on: bool=True):
    if not turn_on:
        dpg.hide_item('request_download_progress')
        dpg.set_value('request_download_progress', "")

        dpg.hide_item('request_download_speed')
        dpg.set_value('request_download_speed', "")

        dpg.hide_item('request_download_elapsed')
        dpg.set_value('request_download_elapsed', "")
    else:
        dpg.show_item('request_download_progress')
        dpg.show_item('request_download_speed')
        dpg.show_item('request_download_elapsed')