import os
import re
from pytubefix import YouTube
from tqdm import tqdm
from moviepy import VideoFileClip, AudioFileClip


# İlerleme çubuğunu güncelleyen fonksiyon
def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    bar.n = bytes_downloaded  # Güncellenen indirme miktarını belirt
    bar.refresh()  # İlerleme çubuğunu güncelle


def clean_filename(filename):
    # Geçersiz karakterleri temizle
    return re.sub(r'[<>:"/\\|?*]', '', filename)


def youtube_video_downloader(url):
    try:
        # YouTube objesi oluştur ve ilerleme çubuğunu bağla
        yt = YouTube(url, on_progress_callback=on_progress)

        # Kullanılabilir tüm video akışlarını listele (adaptive dahil)
        video_streams = yt.streams.filter(progressive=False, file_extension='mp4', type='video').order_by(
            'resolution').desc()
        audio_streams = yt.streams.filter(only_audio=True).order_by('abr').desc()

        print("Kullanılabilir video çözünürlükleri:")
        for i, stream in enumerate(video_streams):
            print(f"{i + 1}. {stream.resolution} - {stream.filesize // (1024 * 1024)} MB")

        video_choice = int(input("İndirmek istediğiniz video çözünürlüğü numarasını seçin: ")) - 1
        video = video_streams[video_choice]

        print("Kullanılabilir ses akışları:")
        for i, stream in enumerate(audio_streams):
            print(f"{i + 1}. {stream.abr} - {stream.filesize // (1024 * 1024)} MB")

        audio_choice = int(input("İndirmek istediğiniz ses akışı numarasını seçin: ")) - 1
        audio = audio_streams[audio_choice]

        print(f"\nVideo indiriliyor: {yt.title} ({video.resolution})")

        # İlerleme çubuğu başlat
        global bar
        bar = tqdm(total=video.filesize, unit='B', unit_scale=True, desc="Video İndirme İlerliyor")

        # Masaüstü yolunu al ve videoyu masaüstüne indir
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        clean_title = clean_filename(yt.title)
        video_file_path = os.path.join(desktop_path, f"{clean_title}_video.mp4")
        audio_file_path = os.path.join(desktop_path, f"{clean_title}_audio.mp4")

        video.download(output_path=desktop_path, filename=f"{clean_title}_video.mp4")
        bar.close()

        print(f"\nSes indiriliyor: {yt.title} ({audio.abr})")
        bar = tqdm(total=audio.filesize, unit='B', unit_scale=True, desc="Ses İndirme İlerliyor")
        audio.download(output_path=desktop_path, filename=f"{clean_title}_audio.mp4")
        bar.close()

        # Dosyaların varlığını kontrol et
        if not os.path.exists(video_file_path):
            print(f"Hata: Video dosyası bulunamadı: {video_file_path}")
            return
        if not os.path.exists(audio_file_path):
            print(f"Hata: Ses dosyası bulunamadı: {audio_file_path}")
            return

        # Videoyu ve sesi birleştir
        print("Video ve ses birleştiriliyor...")
        final_video = VideoFileClip(video_file_path)
        final_audio = AudioFileClip(audio_file_path)
        final_video.set_audio(final_audio)
        final_video_file_path = os.path.join(desktop_path, f"{clean_title}_final.mp4")
        final_video.write_videofile(final_video_file_path, codec='libx264')

        print("\nİndirme ve birleştirme tamamlandı! Video masaüstüne kaydedildi.")
    except Exception as e:
        print("Bir hata oluştu:", e)


# Kullanıcıdan URL al
url = input("İndirmek istediğiniz YouTube video URL'sini girin: ")
youtube_video_downloader(url)
