import time
import os
import tempfile
import zipfile
import platform
import subprocess
from moviepy.editor import (AudioFileClip, CompositeVideoClip, CompositeAudioClip, ImageClip,
                            TextClip, VideoFileClip)
from moviepy.audio.fx.audio_loop import audio_loop
from moviepy.audio.fx.audio_normalize import audio_normalize
from moviepy.config import change_settings
import requests

def download_file(url, filename):
    with open(filename, 'wb') as f:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        f.write(response.content)

def search_program(program_name):
    try: 
        search_cmd = "where" if platform.system() == "Windows" else "which"
        return subprocess.check_output([search_cmd, program_name]).decode().strip()
    except subprocess.CalledProcessError:
        return None

def get_program_path(program_name):
    program_path = search_program(program_name)
    return program_path

def get_output_media(audio_file_path, timed_captions, background_video_data, video_server):
    OUTPUT_FILE_NAME = "rendered_video.mp4"

    # ✅ STEP 1: VERIFY IMAGEMAGICK PATH
    # Unga PC la endha path la iruko, adha inga podunga!
    # Common paths:
    # r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"
    # r"C:\Program Files\ImageMagick-7.1.3-Q16-HDRI\magick.exe"
    magick_path = r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe" 
    
    if os.path.exists(magick_path):
        print(f"✅ Found ImageMagick at: {magick_path}")
        change_settings({"IMAGEMAGICK_BINARY": magick_path})
    else:
        print(f"❌ ImageMagick NOT found at: {magick_path}")
        print("Please install ImageMagick and update the path in render_engine.py")

    visual_clips = []
    downloaded_files = [] # To keep track for cleanup

    print("📥 Downloading background videos...")
    
    for (t1, t2), video_url in background_video_data:
        try:
            # Download the video file
            video_filename = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4').name
            download_file(video_url, video_filename)
            downloaded_files.append(video_filename)

            # Create VideoFileClip
            video_clip = VideoFileClip(video_filename)
            video_clip = video_clip.set_start(t1)
            video_clip = video_clip.set_end(t2)
            
            # Resize logic (Optional: Ensures all videos are 1080p)
            # video_clip = video_clip.resize(height=1080) 
            
            visual_clips.append(video_clip)
        except Exception as e:
            print(f"⚠️ Error processing video segment {t1}-{t2}: {e}")
            continue

    if not visual_clips:
        raise Exception("No video clips were loaded! Check internet or Pexels API.")

    # Load Audio
    audio_file_clip = AudioFileClip(audio_file_path)
    
    # ✅ STEP 2: CAPTIONS LOGIC (UPDATED)
    print("📝 Generating text overlays...")
    for (t1, t2), text in timed_captions:
        if not text.strip():
            continue
            
        try:
            text_clip = TextClip(
                txt=text, 
                fontsize=70, 
                color="white", 
                stroke_width=2, 
                stroke_color="black", 
                font="Arial", 
                method="caption", 
                size=(1920*0.8, None) # 80% of screen width
            )
            text_clip = text_clip.set_start(t1)
            text_clip = text_clip.set_end(t2)
            text_clip = text_clip.set_position(("center", "bottom")) # Safe position
            visual_clips.append(text_clip)
        except Exception as e:
            print(f"⚠️ Error creating text clip '{text}': {e}")
            # Continue without this text clip, don't crash

    # ✅ STEP 3: COMPOSITE VIDEO
    print("🎬 Stitching video together...")
    video = CompositeVideoClip(visual_clips)

    # Set Audio
    video.audio = audio_file_clip
    video.duration = audio_file_clip.duration

    # Write Output
    video.write_videofile(OUTPUT_FILE_NAME, codec='libx264', audio_codec='aac', fps=24, preset='veryfast')

    # ✅ STEP 4: CLEANUP
    print("🧹 Cleaning up temp files...")
    for f in downloaded_files:
        try:
            os.remove(f)
        except:
            pass

    return OUTPUT_FILE_NAME