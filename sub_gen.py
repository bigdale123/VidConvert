from threading import Thread
from concurrent.futures import ThreadPoolExecutor
from discord_webhook import DiscordWebhook
import sys
import os
import shutil
import queue
import re

preset_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "presets.json")

# def convertVideo(video_file):
#     temp_file = os.path.join(os.path.dirname(video_file), f"temp_file.mkv")
#     os.system(f"HandBrakeCLI -i \"{video_file}\" -o \"{temp_file}\" --preset-import-file \"{preset_file}\" --preset \"Fast 1080p NVENC\"")
#     shutil.move(temp_file, video_file)
#     return

def convert_sub(file):
    os.system(f"faster-whisper-xxl.exe \"{file}\" --verbose true --language English --model medium -o \"{os.path.dirname(file)}\"")
    return

def extractSubtitles(file):
    base_name = os.path.splitext(os.path.basename(file))[0]
    # print(base_name)

    pattern = re.compile(re.escape(base_name) + r'\.\w*\.srt', re.IGNORECASE)
    exists = False
    for srt_file in os.listdir(os.path.dirname(file)):
        # print(srt_file)
        # print(pattern.match(srt_file))
        if pattern.match(srt_file):
            exists = True
            break
    if exists or os.path.isfile(file[:-3]+"srt"):
        print("Found Existing SRT file, doing nothing.")
    else:
        convert_sub(file)
    return

def getFiles(folder):
    files = []
    try:
        for root, dirs, files_in_dir in os.walk(folder):
            for file in files_in_dir:
                if file.endswith(".mkv") or file.endswith(".mp4") or file.endswith(".avi"):
                    files.append(os.path.join(root, file))
        return files

    except OSError as e:
        print(f"Error reading files in folder {folder}: {e}")
        return files

if __name__ == "__main__":
    files = getFiles(sys.argv[1])
    NUM_WORKERS = 4
    with ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
        futures = [executor.submit(extractSubtitles, file) for file in files]
        for future in futures:
            future.result()

    # for file in files:
    #     extractSubtitles(file)

    DiscordWebhook(url='https://discord.com/api/webhooks/1007306451783516261/qgy4EPGLhVN5Bc_bYWvBMw1I0RfK-N_7Zpm0aSbofQZL2EzYJ_7Pc7ahIcfKoJ5Be72l', content="Subs Are Done.").execute()