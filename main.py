import flet as ft
import yt_dlp
import os
import static_ffmpeg

# FFmpeg-ийг системд бүртгэх (Android-д зориулсан чухал хэсэг)
try:
    static_ffmpeg.add_paths()
except:
    pass

def main(page: ft.Page):
    page.title = "pon pon app"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.scroll = ft.ScrollMode.ADAPTIVE 

    url_input = ft.TextField(label="YouTube Линк", hint_text="Энд линкээ наана уу...", expand=True)
    
    quality_dropdown = ft.Dropdown(
        label="Чанараа сонгоно уу",
        options=[
            ft.dropdown.Option("1080", "Full HD (1080p)"),
            ft.dropdown.Option("720", "HD (720p)"),
            ft.dropdown.Option("audio", "Зөвхөн Дуу (MP3)"),
        ],
        value="1080",
    )

    status_text = ft.Text("Бэлэн", color=ft.Colors.CYAN)
    percent_text = ft.Text("0%", size=25, weight="bold", color=ft.Colors.GREEN_ACCENT)
    pb = ft.ProgressBar(width=400, value=0, visible=False, color=ft.Colors.GREEN_ACCENT)

    def progress_hook(d):
        if d['status'] == 'downloading':
            # Хувийг илүү найдвартай салгах
            p = d.get('_percent_str', '0%').replace('%','').strip()
            try:
                float_p = float(p)
                pb.value = float_p / 100
                percent_text.value = f"{float_p}%"
                status_text.value = "Татаж байна..."
                page.update()
            except:
                pass
        elif d['status'] == 'finished':
            status_text.value = "Боловсруулж байна (FFmpeg)..."
            page.update()

    def download_click(e):
        url = url_input.value
        if not url:
            status_text.value = "Линкээ оруулна уу!"
            page.update()
            return
        
        quality = quality_dropdown.value
        status_text.value = "Холбогдож байна..."
        status_text.color = ft.Colors.YELLOW
        pb.visible = True
        pb.value = 0
        percent_text.value = "0%"
        page.update()

        # Хадгалах зам тохируулах
        if os.name == 'nt': # Windows
            save_path = os.path.join(os.path.expanduser("~"), "Downloads")
        else: # Android
            save_path = '/storage/emulated/0/Download'

        # Сонгосон чанарт тааруулах
        if quality == "audio":
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
        else:
            ydl_opts = {
                'format': f'bestvideo[height<={quality}]+bestaudio/best',
                'merge_output_format': 'mp4',
            }

        # Нийтлэг тохиргоонууд
        ydl_opts.update({
            'progress_hooks': [progress_hook],
            'outtmpl': f'{save_path}/%(title)s.%(ext)s',
            'noplaylist': True,
        })

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            status_text.value = "Амжилттай татлаа! (Downloads хавтаст)"
            status_text.color = ft.Colors.GREEN
            percent_text.value = "100%"
            pb.value = 1
        except Exception as ex:
            status_text.value = f"Алдаа: {str(ex)}"
            status_text.color = ft.Colors.RED
        
        page.update()

    page.add(
        ft.Text("pon pon app", size=35, weight="bold", color=ft.Colors.BLUE_ACCENT),
        ft.Divider(),
        ft.Row([url_input, ft.IconButton(ft.Icons.CLEAR, on_click=lambda _: (setattr(url_input, "value", ""), page.update()))]),
        quality_dropdown,
        ft.Container(height=10),
        ft.ElevatedButton(
            "ТАТАЖ ЭХЛЭХ", 
            on_click=download_click, 
            width=400, 
            height=60,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
        ),
        ft.Container(height=20),
        ft.Column([
            status_text,
            pb,
            ft.Alignment(percent_text, alignment=ft.alignment.center),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

if __name__ == "__main__":
    ft.app(target=main)
