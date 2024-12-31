import os
import subprocess


def merge_video_audio_ffmpeg(video_filename, audio_filename, output_filename):
    try:
        # Video ve ses dosyalarının varlığını kontrol et
        if not os.path.exists(video_filename):
            print(f"Hata: Video dosyası bulunamadı: {video_filename}")
            return
        if not os.path.exists(audio_filename):
            print(f"Hata: Ses dosyası bulunamadı: {audio_filename}")
            return

        # ffmpeg komutunu çalıştırarak video ve ses birleştirme işlemi
        command = [
            'ffmpeg', '-i', video_filename, '-i', audio_filename,
            '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental', output_filename
        ]
        subprocess.run(command, check=True)
        print(f"Birleştirme tamamlandı! Video kaydedildi: {output_filename}")

    except subprocess.CalledProcessError as e:
        print("Birleştirme sırasında bir hata oluştu:", e)
    except Exception as e:
        print("Bir hata oluştu:", e)


# Masaüstü yolunu ayarla
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# Video ve ses dosyalarının isimlerini belirt
video_file_path = os.path.join(desktop_path, "En İyi Not Alma Yöntemi Hangisi  Yalçın Arsan & Hakan Koç_video.mp4")  # Video dosya adını buraya yaz
audio_file_path = os.path.join(desktop_path, "En İyi Not Alma Yöntemi Hangisi  Yalçın Arsan & Hakan Koç_audio.mp4")  # Ses dosya adını buraya yaz
output_file_path = os.path.join(desktop_path, "birlesmis_video.mp4")  # Çıktı dosya adı

# Birleştirme işlemini başlat
merge_video_audio_ffmpeg(video_file_path, audio_file_path, output_file_path)

merge_video_audio_ffmpeg(video_file_path, audio_file_path, output_file_path)
