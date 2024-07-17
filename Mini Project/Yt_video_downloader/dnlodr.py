import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pytube import YouTube
import threading

def on_progress(stream, chunk, bytes_remaining, progress_bar):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    progress_bar['value'] = percentage_of_completion

def download_video(url, progress_bar, progress_label):
    try:
        yt = YouTube(url, on_progress_callback=lambda stream, chunk, bytes_remaining: on_progress(stream, chunk, bytes_remaining, progress_bar))
        stream = yt.streams.get_highest_resolution()
        
        folder_path = filedialog.askdirectory()
        
        if folder_path:
            progress_label.config(text="Download started...")
            stream.download(folder_path)
            progress_label.config(text="Download completed successfully!")
        else:
            progress_label.config(text="Download cancelled.")
    except Exception as e:
        progress_label.config(text="Error in downloading the video.")
        messagebox.showerror("Error", str(e))

def start_downloads():
    links = [entry.get() for entry in link_entries if entry.get()]
    for link, progress_bar, progress_label in zip(links, progress_bars, progress_labels):
        threading.Thread(target=download_video, args=(link, progress_bar, progress_label)).start()

def add_link_entry():
    link_label = tk.Label(scrollable_frame, text=f"Link {len(link_entries) + 1}:", bg='#0ff')
    link_label.pack(pady=(10, 5), anchor="center")
    
    link_entry = tk.Entry(scrollable_frame, width=50)
    link_entry.pack(pady=5, anchor="center")
    
    progress_frame = tk.Frame(scrollable_frame, bg='#0ff')
    progress_frame.pack(pady=(5, 10), anchor="center")
    
    progress_bar = ttk.Progressbar(progress_frame, orient=tk.HORIZONTAL, length=200, mode='determinate')
    progress_bar.pack(pady=5)
    
    progress_label = tk.Label(progress_frame, text="Waiting for download...", bg='#0ff')
    progress_label.pack()
    
    link_entries.append(link_entry)
    progress_bars.append(progress_bar)
    progress_labels.append(progress_label)

root = tk.Tk()
root.title("YtDnld")
root.geometry("420x420")
root.configure(bg='#1f1f1f')

canvas = tk.Canvas(root, bg='#0ff')
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg='#0ff')

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

link_entries = []
progress_bars = []
progress_labels = []

for _ in range(1):
    add_link_entry()

add_button = tk.Button(scrollable_frame, text="Add another link", command=add_link_entry, bg='#0ff')
add_button.pack(pady=20, anchor="center")

download_button = tk.Button(scrollable_frame, text="Download", command=start_downloads, bg='#0ff')
download_button.pack(pady=20, anchor="center")

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Run
root.mainloop()




 