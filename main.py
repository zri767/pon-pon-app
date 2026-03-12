import flet as ft
import yt_dlp
import os
import static_ffmpeg
static_ffmpeg.add_paths() # Энэ нь ffmpeg-ийг апп дотор ажиллагаанд оруулна
def main(page: ft.Page):
    page.title = "pon pon app"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.window_width = 400
    page.window_height = 700

    url_input = ft.TextField(label="YouTube Линк", hint_text="https://...", expand=True)
    
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
            p = d.get('_percent_str', '0%').replace('%','').strip()
            try:
                float_p = float(p)
                pb.value = float_p / 100
                percent_text.value = f"{float_p}%"
                page.update()
            except: pass
        elif d['status'] == 'finished':
            status_text.value = "Боловсруулж байна..."
            page.update()

    def download_click(e):
        url = url_input.value
        if not url:
            status_text.value = "Линкээ оруулна уу!"
            page.update()
            return
        
        status_text.value = "Холбогдож байна..."
        pb.visible = True
        pb.value = 0
        page.update()

        # Android дээрх хадгалах замыг тодорхойлох
        # Хэрэв үндсэн Download хавтас руу хандаж чадахгүй бол апп-ын доторх хавтаст хадгална
        possible_paths = [
            '/storage/emulated/0/Download',
            os.path.join(os.path.expanduser("~"), "Downloads"),
            "."
        ]
        
        save_path = "."
        for p in possible_paths:
            if os.path.exists(p) and os.access(p, os.W_OK):
                save_path = p
                break

        ydl_opts = {
            'format': f'bestvideo[height<={quality_dropdown.value}]+bestaudio/best' if quality_dropdown.value != "audio" else 'bestaudio/best',
            'outtmpl': f'{save_path}/%(title)s.%(ext)s',
            'progress_hooks': [progress_hook],
            'noplaylist': True,
        }

        if quality_dropdown.value == "audio":
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            status_text.value = f"Амжилттай татлаа! Зам: {save_path}"
            status_text.color = ft.Colors.GREEN
        except Exception as ex:
            status_text.value = f"Алдаа: {str(ex)}"
            status_text.color = ft.Colors.RED
        
        page.update()

    page.add(
        ft.Text("pon pon app", size=30, weight="bold"),
        ft.Row([url_input, ft.IconButton(ft.Icons.CLEAR, on_click=lambda _: (setattr(url_input, "value", ""), page.update()))]),
        quality_dropdown,
        ft.ElevatedButton("ТАТАЖ ЭХЛЭХ", on_click=download_click, width=400, height=60),
        status_text,
        ft.Column([pb, percent_text], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

if __name__ == "__main__":
    ft.app(target=main)
