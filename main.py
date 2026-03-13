import flet as ft
import yt_dlp
import os
import static_ffmpeg

# Зай авалтгүйгээр эхлүүлнэ
static_ffmpeg.add_paths()

def main(page: ft.Page):
    page.title = "Pon Pon Downloader"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 450
    page.window_height = 800
    page.scroll = ft.ScrollMode.ADAPTIVE

    # Түүх хадгалах жагсаалт
    history_list = ft.Column()

    # Прогресс баар болон бамбарууш
    pb = ft.ProgressBar(width=400, color="pink", bgcolor="#eeeeee", value=0)
    progress_text = ft.Text("0%", size=20, weight="bold")
    bear_icon = ft.Text("🐻", size=30) # Гүйж байгаа бамбарууш

    def progress_hook(d):
        if d['status'] == 'downloading':
            p = d.get('_percent_str', '0%').replace('%','')
            try:
                float_p = float(p) / 100
                pb.value = float_p
                progress_text.value = f"{p}%"
                # Бамбаруушийг гүйлгэх (зай авах)
                bear_icon.padding = ft.padding.only(left=float_p * 350)
                page.update()
            except:
                pass
        elif d['status'] == 'finished':
            pb.value = 1
            progress_text.value = "100% - Боловсруулж байна..."
            page.update()

    def download_click(e):
        url = url_input.value
        if not url:
            status_text.value = "Линкээ оруулна уу!"
            status_text.color = "red"
            page.update()
            return

        # Түүхэнд нэмэх
        history_list.controls.insert(0, ft.ListTile(title=ft.Text(url, max_lines=1), leading=ft.Icon(ft.icons.HISTORY)))
        
        save_path = '/storage/emulated/0/Download' # Android үндсэн татах хавтас
        
        quality = quality_dropdown.value
        ydl_opts = {
            'format': f'bestvideo[height<={quality}]+bestaudio/best' if quality != "audio" else 'bestaudio/best',
            'outtmpl': f'{save_path}/%(title)s.%(ext)s',
            'progress_hooks': [progress_hook],
            'merge_output_format': 'mp4',
        }

        try:
            status_text.value = "Татаж байна..."
            status_text.color = "blue"
            page.update()
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            status_text.value = f"Амжилттай! Хадгалсан: {save_path}"
            status_text.color = "green"
        except Exception as ex:
            status_text.value = f"Алдаа: {str(ex)}"
            status_text.color = "red"
        page.update()

    # Интерфэйс
    url_input = ft.TextField(label="YouTube Линк", border_color="pink")
    quality_dropdown = ft.Dropdown(
        label="Чанар сонгох",
        options=[
            ft.dropdown.Option("360"),
            ft.dropdown.Option("720"),
            ft.dropdown.Option("1080"),
            ft.dropdown.Option("audio", "Зөвхөн Дуу"),
        ],
        value="720"
    )
    status_text = ft.Text()

    page.add(
        ft.Text("Pon Pon App 🐻", size=30, weight="bold", color="pink"),
        url_input,
        quality_dropdown,
        ft.ElevatedButton("Татаж эхлэх", on_click=download_click, bgcolor="pink", color="white"),
        status_text,
        ft.Column([bear_icon, pb, progress_text], horizontal_alignment="center"),
        ft.Divider(),
        ft.Text("Таталтын түүх:", weight="bold"),
        history_list
    )

ft.app(target=main)
