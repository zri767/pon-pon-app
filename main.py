import flet as ft
import yt_dlp
import os
import threading

def main(page: ft.Page):
    page.title = "Pon Pon App 🐻"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = ft.ScrollMode.ADAPTIVE

    history_list = ft.Column()
    pb = ft.ProgressBar(width=400, value=0)
    progress_text = ft.Text("0%")
    status_text = ft.Text()

    def progress_hook(d):
        if d['status'] == 'downloading':
            p = d.get('_percent_str', '0%').replace('%','')
            try:
                pb.value = float(p) / 100
                progress_text.value = f"{p}%"
                page.update()
            except:
                pass

    def start_download():

        url = url_input.value
        if not url:
            status_text.value = "Линкээ оруулна уу!"
            page.update()
            return

        save_path = os.path.join(os.getcwd(), "downloads")
        os.makedirs(save_path, exist_ok=True)

        ydl_opts = {
            'format': 'best',
            'outtmpl': f'{save_path}/%(title)s.%(ext)s',
            'progress_hooks': [progress_hook],
        }

        try:
            status_text.value = "Татаж байна..."
            page.update()

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            status_text.value = "Амжилттай татлаа!"
        except Exception as ex:
            status_text.value = str(ex)

        page.update()

    def download_click(e):
        threading.Thread(target=start_download).start()

    url_input = ft.TextField(label="YouTube линк")

    page.add(
        ft.Text("Pon Pon App 🐻", size=25),
        url_input,
        ft.ElevatedButton("Татах", on_click=download_click),
        pb,
        progress_text,
        status_text,
        history_list
    )

ft.app(target=main)
