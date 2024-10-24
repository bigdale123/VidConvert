from threading import Thread
from discord_webhook import DiscordWebhook
import sys
import subprocess
import os
import shutil
import queue
import re
import platform

preset_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "presets.json")

def convertVideo(video_file):
    temp_file = os.path.join(os.path.dirname(video_file), "temp_file.mkv")
    new_file = os.path.join(os.path.dirname(video_file), "new_file.mkv")
    os.system(f"HandBrakeCLI -i \"{video_file}\" -o \"{temp_file}\" --preset-import-file \"{preset_file}\" --preset \"Fast 1080p NVENC\"")
    os.system(f"mkvmerge -o \"{new_file}\" -D -A \"{video_file}\" -S -B -T -M \"{temp_file}\"")
    shutil.move(new_file, video_file)
    os.remove(temp_file)
    return

def check_h264(path):
    ffprobe_command = str(subprocess.check_output(["ffprobe",
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=codec_name",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        f"{path}"
    ]))
    return "h264" in ffprobe_command

def getFiles(folder):
    compatible_files = [
        "mkv",
        "mp4",
        "avi",
        "webm",
        "m4v"
    ]
    files = []
    try:
        for root, dirs, files_in_dir in os.walk(folder):
            for file in files_in_dir:
                if file.split(".")[-1] in compatible_files:# and not check_h264(os.path.join(root, file)):
                    files.append(os.path.join(root, file))
        return files

    except OSError as e:
        print(f"Error reading files in folder {folder}: {e}")
        return files

if __name__ == "__main__":
    files = getFiles(sys.argv[1])

    for file in files:
        convertVideo(file)
    
    DiscordWebhook(url='https://discord.com/api/webhooks/1007306451783516261/qgy4EPGLhVN5Bc_bYWvBMw1I0RfK-N_7Zpm0aSbofQZL2EzYJ_7Pc7ahIcfKoJ5Be72l', content=f"VidConvert on {platform.uname().node} ({platform.uname().system}) has Finished.").execute()
