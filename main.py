import flet as ft
import yt_dlp
import os

def main(page: ft.Page):
    page.title = "pon pon app"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    # Утасны дэлгэцэнд тааруулж scroll нэмэв
    page.scroll = ft.ScrollMode.ADAPTIVE 

    url_input = ft.TextField(label="Видео линк", hint_text="https://...", expand=True)
    
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
    percent_text = ft.Text("0%", size=20, weight="bold", color=ft.Colors.GREEN_ACCENT)
    pb = ft.ProgressBar(width=400, value=0, visible=False, color=ft.Colors.GREEN_ACCENT)

    def progress_hook(d):
        if d['status'] == 'downloading':
            p_str = d.get('_percent_str', '0%').replace('%','').strip()
            try:
                p_val = float(p_str)
                pb.value = p_val / 100
                percent_text.value = f"{p_val}%"
                page.update()
            except: pass
        elif d['status'] == 'finished':
            status_text.value = "Боловсруулж байна..."
            page.update()

    def download_click(e):
        url = url_input.value
        if not url: return
        
        quality = quality_dropdown.value
        status_text.value = "Холбогдож байна..."
        pb.visible = True
        page.update()

        # Гар утасны "Download" хавтас руу хадгалах зам
        if os.name == 'nt':
            save_path = os.path.join(os.path.expanduser("~"), "Downloads")
        else:
            # Android-д зориулсан стандарт зам
            save_path = '/storage/emulated/0/Download'

        ydl_opts = {
            'format': f'bestvideo[height<={quality}]+bestaudio/best',
            'progress_hooks': [progress_hook],
            'outtmpl': f'{save_path}/%(title)s.%(ext)s',
            'merge_output_format': 'mp4',
            # Android дээр ffmpeg-ийг автоматаар хайх тул location заах шаардлагагүй байж болно
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            status_text.value = "Амжилттай татлаа!"
            status_text.color = ft.Colors.GREEN
        except Exception as ex:
            status_text.value = f"Алдаа: {str(ex)}"
        
        page.update()

    page.add(
        ft.Text("pon pon app", size=32, weight="bold"),
        ft.Row([url_input, ft.IconButton(ft.Icons.DELETE_OUTLINE, on_click=lambda _: (setattr(url_input, "value", ""), page.update()))]),
        quality_dropdown,
        ft.ElevatedButton("ТАТАЖ ЭХЛЭХ", on_click=download_click, width=400, height=60),
        status_text,
        ft.Row([pb, percent_text], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    )

if __name__ == "__main__":
    # Утас дээр ажиллахад зориулсан тохиргоо
    ft.app(target=main)
