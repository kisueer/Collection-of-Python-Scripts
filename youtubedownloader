import os
import sys
import re
from datetime import datetime
import urllib.request
import urllib.error
import subprocess

# Let's use yt-dlp instead of pytube as it's more reliable and handles YouTube changes better
try:
    import yt_dlp
except ImportError:
    print("The 'yt-dlp' library is required. Please install it using:")
    print("pip install yt-dlp")
    sys.exit(1)

def sanitize_filename(filename):
    """Remove invalid characters from filename"""
    # Replace invalid characters with underscore
    return re.sub(r'[\\/*?:"<>|]', "_", filename)

def download_video(url, output_path=None):
    try:
        # Set output path
        if output_path is None:
            output_path = os.getcwd()
        
        # Ensure the output directory exists
        os.makedirs(output_path, exist_ok=True)
        
        # Configure yt-dlp options
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'restrictfilenames': True,
            'noplaylist': True,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': False,
            'no_warnings': False,
            'default_search': 'auto',
            'source_address': '0.0.0.0',
        }
        
        # Create a download progress hook
        def progress_hook(d):
            if d['status'] == 'downloading':
                if 'total_bytes' in d and 'downloaded_bytes' in d:
                    percent = d['downloaded_bytes'] / d['total_bytes'] * 100
                    print(f"\rDownloading: {percent:.1f}% of {d['_total_bytes_str']}", end='')
                else:
                    print(f"\rDownloading: {d['_percent_str']} of {d['_total_bytes_str']}", end='')
            elif d['status'] == 'finished':
                print("\nDownload complete! Converting...")
        
        ydl_opts['progress_hooks'] = [progress_hook]
        
        # Download the video
        print(f"Fetching video information...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            print(f"\nTitle: {info.get('title', 'Unknown')}")
            print(f"Duration: {info.get('duration', 0)} seconds")
            print(f"Channel: {info.get('uploader', 'Unknown')}")
            print(f"\nStarting download to {output_path}...")
            
            ydl.download([url])
            
            # Get the output filename
            video_title = sanitize_filename(info.get('title', 'video'))
            out_file = os.path.join(output_path, f"{video_title}.mp4")
            
            print(f"\nVideo saved to: {out_file}")
            return out_file
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        if "HTTP Error 429" in str(e):
            print("YouTube is rate limiting your requests. Try again later.")
        elif "HTTP Error 403" in str(e):
            print("Access forbidden. YouTube might have blocked your IP or the video requires authentication.")
        return None

def download_audio(url, output_path='G:\code\kisu\scripts\output\youtube\mp3', ffmpeg_path=None):
    try:
        # Set output path
        if output_path is None:
            output_path = 'G:\code\kisu\scripts\output\youtube\mp3'
        
        # Ensure the output directory exists
        os.makedirs(output_path, exist_ok=True)
        
        # Check for FFmpeg
        has_ffmpeg = False
        if ffmpeg_path:
            # Use provided FFmpeg path
            has_ffmpeg = os.path.exists(ffmpeg_path)
        else:
            # Try to auto-detect FFmpeg
            try:
                with open(os.devnull, 'w') as devnull:
                    subprocess.check_call(['ffmpeg', '-version'], stdout=devnull, stderr=devnull)
                has_ffmpeg = True
            except (subprocess.SubprocessError, FileNotFoundError):
                has_ffmpeg = False
        
        # Configure yt-dlp options based on FFmpeg availability
        if has_ffmpeg:
            print("FFmpeg found - will convert to MP3")
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'extractaudio': True,
                'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                'restrictfilenames': True,
                'noplaylist': True,
                'nocheckcertificate': True,
                'ignoreerrors': False,
                'logtostderr': False,
                'quiet': False,
                'no_warnings': False,
                'default_search': 'auto',
                'source_address': '0.0.0.0',
            }
            
            # Use provided FFmpeg path if specified
            if ffmpeg_path:
                ydl_opts['ffmpeg_location'] = ffmpeg_path
        else:
            print("FFmpeg not found - downloading audio in original format")
            # Download audio without conversion
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                'restrictfilenames': True,
                'noplaylist': True,
                'nocheckcertificate': True,
                'postprocessors': [],  # No post-processing without FFmpeg
                'ignoreerrors': False,
                'logtostderr': False,
                'quiet': False,
                'no_warnings': False,
                'default_search': 'auto',
                'source_address': '0.0.0.0',
            }
        
        # Create a download progress hook
        def progress_hook(d):
            if d['status'] == 'downloading':
                if 'total_bytes' in d and 'downloaded_bytes' in d:
                    percent = d['downloaded_bytes'] / d['total_bytes'] * 100
                    print(f"\rDownloading: {percent:.1f}% of {d['_total_bytes_str']}", end='')
                else:
                    print(f"\rDownloading: {d['_percent_str']} of {d['_total_bytes_str']}", end='')
            elif d['status'] == 'finished':
                print("\nDownload complete!" + (" Converting to MP3..." if has_ffmpeg else ""))
        
        ydl_opts['progress_hooks'] = [progress_hook]
        
        # Download and convert to MP3 if FFmpeg is available
        print(f"Fetching video information...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            print(f"\nTitle: {info.get('title', 'Unknown')}")
            print(f"Duration: {info.get('duration', 0)} seconds")
            print(f"Channel: {info.get('uploader', 'Unknown')}")
            print(f"\nStarting download to {output_path}...")
            
            ydl.download([url])
            
            # Get the output filename
            audio_title = sanitize_filename(info.get('title', 'audio'))
            extension = 'mp3' if has_ffmpeg else info.get('ext', 'webm')
            out_file = os.path.join(output_path, f"{audio_title}.{extension}")
            
            print(f"\nAudio saved to: {out_file}")
            
            # If FFmpeg wasn't available, provide installation instructions
            if not has_ffmpeg:
                print("\nNote: FFmpeg was not found on your system. To convert to MP3 format, please install FFmpeg:")
                print("- Windows: Download from https://ffmpeg.org/download.html or install with 'chocolatey install ffmpeg'")
                print("- Mac: 'brew install ffmpeg'")
                print("- Linux: 'apt-get install ffmpeg' or equivalent for your distribution")
                print("\nAlternatively, you can specify the path to your FFmpeg executable using:")
                print(f"python {sys.argv[0]} audio {url} {output_path} --ffmpeg-path C:\\path\\to\\ffmpeg.exe")
            
            return out_file
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        if "HTTP Error 429" in str(e):
            print("YouTube is rate limiting your requests. Try again later.")
        elif "HTTP Error 403" in str(e):
            print("Access forbidden. YouTube might have blocked your IP or the video requires authentication.")
        elif "ffprobe" in str(e) or "ffmpeg" in str(e):
            print("\nFFmpeg error: To use MP3 conversion, please install FFmpeg:")
            print("- Windows: Download from https://ffmpeg.org/download.html or install with 'chocolatey install ffmpeg'")
            print("- Mac: 'brew install ffmpeg'")
            print("- Linux: 'apt-get install ffmpeg' or equivalent for your distribution")
            print("\nAlternatively, you can specify the path to your FFmpeg executable using:")
            print(f"python {sys.argv[0]} audio {url} {output_path} --ffmpeg-path C:\\path\\to\\ffmpeg.exe")
        return None

def main():

    # Simple command line interface
    if len(sys.argv) < 2:
        print("Usage:")
        print("  For video: python youtube_downloader.py video <youtube_url> [output_path]")
        print("  For audio: python youtube_downloader.py audio <youtube_url> [output_path] [--ffmpeg-path PATH]")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command not in ["video", "audio"]:
        print("Invalid command. Use 'video' or 'audio'.")
        sys.exit(1)
    
    if len(sys.argv) < 3:
        print("Please provide a YouTube URL.")
        sys.exit(1)
    
    url = sys.argv[2]
    output_path = None
    ffmpeg_path = None
    
    # Process additional arguments
    for i in range(3, len(sys.argv)):
        if sys.argv[i] == "--ffmpeg-path" and i + 1 < len(sys.argv):
            ffmpeg_path = sys.argv[i + 1]
        elif not sys.argv[i].startswith("--") and output_path is None:
            output_path = sys.argv[i]
    
    # Use current directory as default output path
    if output_path is None:
        output_path = os.getcwd()
    
    if command == "video":
        download_video(url, output_path)
    else:
        download_audio(url, output_path, ffmpeg_path)

if __name__ == "__main__":
    main()
