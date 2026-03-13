import flet as ft
import yt_dlp
import os
import static_ffmpeg

# ffmpeg-ийг системд бүртгэх
try:
    static_ffmpeg.add_paths()
except:
    pass

def main(page: ft.Page):
    page.title = "Pon Pon App 🐻"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = ft.ScrollMode.ADAPTIVE
    
    # Апп асах үед хадгалах зөвшөөрөл нэхэх
    def on_connect(e):
        page.permission_handler.request_permission(ft.PermissionType.STORAGE)
    
    page.on_connect = on_connect

    history_list = ft.Column()
    pb = ft.ProgressBar(width=400, color="pink", bgcolor="#eeeeee", value=0)
    progress_text = ft.Text("0%", size=16)
    bear_icon = ft.Text("🐻", size=30)

    def progress_hook(d):
        if d['status'] == 'downloading':
            p = d.get('_percent_str', '0%').replace('%','')
            try:
                float_p = float(p) / 100
                pb.value = float_p
                progress_text.value = f"{p}%"
                bear_icon.padding = ft.padding.only(left=min(float_p * 350, 350))
                page.update()
            except:
                pass
        elif d['status'] == 'finished':
            pb.value = 1
            progress_text.value = "Дууслаа! Боловсруулж байна..."
            page.update()

    def download_click(e):
        url = url_input.value
        if not url:
            status_text.value = "Линкээ оруулна уу!"
            status_text.color = "red"
            page.update()
            return

        history_list.controls.insert(0, ft.ListTile(
            title=ft.Text(url, size=12, max_lines=1),
            leading=ft.Icon(ft.icons.HISTORY, color="pink")
        ))
        
        save_path = '/storage/emulated/0/Download'
        if not os.path.exists(save_path):
            save_path = '.'

        quality = quality_dropdown.value
        ydl_opts = {
            'format': f'bestvideo[height<={quality}]+bestaudio/best' if quality != "audio" else 'bestaudio/best',
            'outtmpl': f'{save_path}/%(title)s.%(ext)s',
            'progress_hooks': [progress_hook],
            'nopostoverwrites': False,
        }

        try:
            status_text.value = "Холбогдож байна..."
            status_text.color = "blue"
            page.update()
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            status_text.value = "Амжилттай татлаа! Download хавтсаа шалгана уу."
            status_text.color = "green"
        except Exception as ex:
            status_text.value = f"Алдаа: {str(ex)}"
            status_text.color = "red"
        page.update()

    url_input = ft.TextField(
        label="YouTube Линк", 
        border_color="pink",
        suffix_icon=ft.icons.CLEAR,
        on_submit=download_click
    )
    
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
    
    status_text = ft.Text(size=12)

    page.add(
        ft.Row([ft.Text("Pon Pon App", size=25, weight="bold", color="pink"), ft.Text("🐻", size=25)], alignment="center"),
        url_input,
        quality_dropdown,
        ft.ElevatedButton("Татаж эхлэх", on_click=download_click, bgcolor="pink", color="white"),
        status_text,
        ft.Column([ft.Container(content=bear_icon, width=400), pb, progress_text], horizontal_alignment="center"),
        ft.Divider(),
        ft.Text("Таталтын түүх:", weight="bold"),
        history_list
    )

ft.app(target=main)
