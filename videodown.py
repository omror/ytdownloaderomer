import os
from pytubefix import YouTube
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips

def download_video():
    url = input("YouTube video URL'sini girin: ")
    yt = YouTube(url)

    print("\nVideo Kalite Seçenekleri:")
    video_streams = yt.streams.filter(progressive=False, file_extension='mp4', only_video=True).order_by('resolution').desc()
    for i, stream in enumerate(video_streams):
        print(f"{i + 1}: {stream.resolution} ({stream.fps} fps)")

    video_choice = int(input("\nVideo kalitesini seçin (numara): ")) - 1
    video_stream = video_streams[video_choice]

    print("\nSes Kalite Seçenekleri:")
    audio_streams = yt.streams.filter(only_audio=True, file_extension='mp4').order_by('abr').desc()
    for i, stream in enumerate(audio_streams):
        print(f"{i + 1}: {stream.abr}")

    audio_choice = int(input("\nSes kalitesini seçin (numara): ")) - 1
    audio_stream = audio_streams[audio_choice]

    print("\nİndirme işlemi başlıyor...\n")

    # Video ve Ses İndirme
    video_path = video_stream.download(output_path=".", filename="temp_video.mp4")
    audio_path = audio_stream.download(output_path=".", filename="temp_audio.mp4")

    # Birleştirme İşlemi
    print("Video ve ses birleştiriliyor...")
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_path)
    video_clip = video_clip.set_audio(audio_clip)

    output_filename = yt.title.replace(" ", "_").replace("/", "-") + ".mp4"
    video_clip.write_videofile(output_filename, codec="libx264", audio_codec="aac")

    # Geçici dosyaları silme
    video_clip.close()
    audio_clip.close()
    os.remove(video_path)
    os.remove(audio_path)

    print(f"\nİndirme ve birleştirme işlemi tamamlandı: {output_filename}")

if __name__ == "__main__":
    download_video()
