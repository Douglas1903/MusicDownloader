import time
import yt_dlp
import os
import shutil

source_folder = r"C:\Projetos\automacoes\MusicDownloader"
destination_folder = r"C:\Projetos\automacoes\MusicDownloader\downloaded_songs"
txt_path = r"C:\Projetos\automacoes\MusicDownloader\songs.txt"
insert_link_prompt = "Enter the YouTube video link: "

def download_music(link, destination_folder):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{destination_folder}/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
            'noprogress': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        print(f"Download completed for: {link}")
    except Exception as e:
        print(f"Error downloading music from {link}: {e}")

def handle_files():
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
        
    for file in os.listdir(source_folder):
        if file.endswith(".mp3"):
            source_path = os.path.join(source_folder, file)
            destination_path = os.path.join(destination_folder, file)

            shutil.move(source_path, destination_path)
            print(f"Moved: {file}")

def read_txt_file(txt_path):
    try:
        with open(txt_path, 'r') as file:
            urls = [line.strip() for line in file if line.strip()]
        return urls
    except Exception as e:
        print(f"Error reading the file {txt_path}: {e}")
        return []

def MusicDownloader():
    print('\n(1) Enter URL manually\n(2) Load from a .txt file in the current folder\n(3) Exit the program\n')
    while True:
        mode = input('Type => ').strip()
        
        if mode.lower() == '3':
            print("Exiting the program...")
            break

        if mode == '1':
            link = input(insert_link_prompt)
            folder = destination_folder
            if not folder.strip():
                folder = '.'
            download_music(link, folder)
            handle_files()

        elif mode == '2':
            print('Make sure the txt file is in the current folder')
            time.sleep(2)
            
            txt_path = txt_path.strip()
            urls = read_txt_file(txt_path)
            
            if not urls:
                print("No valid URLs found in the file.")
                print("\nExiting the program...")
                break
            
            print(f"Starting downloads for {len(urls)} URLs...")
            for url in urls:
                download_music(url, destination_folder)
            handle_files()
            print("Processing completed for all URLs.")
            print("\nExiting the program...")
            break
        else:
            print("Invalid option. Please try again.")
