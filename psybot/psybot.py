from pytube import YouTube, Search
from moviepy.editor import VideoFileClip
import os
from tkinter import Tk, Label, Entry, Button, Listbox
from collections import deque
import threading
from pathlib import Path

class EntryWithPlaceholder(Entry):
    def __init__(self, master, width, placeholder="PLACEHOLDER", color='grey'):
        super().__init__(master, width=width)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()

class Psybot:
    WIDTH = 40
    PADDING = 10
    BTN_PADDING = 5

    def __init__(self, master):
        master.title("Psybot")
        self.master = master

        self.queue = deque()

        self.set_ui()

        self.master.bind("<Return>", self.btnAction)

    def set_ui(self):
        self.intro_lbl = Label(self.master, 
                                text="ATENÇÃO! USE APENAS PARA PSYTRANCE",
                                wraplength=200, 
                                justify="center")
        self.intro_lbl.pack(padx=self.PADDING, pady=self.PADDING)

        self.entry = EntryWithPlaceholder(self.master, width=self.WIDTH, placeholder="Insira um baile")
        self.entry.pack(fill="x", padx=self.PADDING)

        self.button = Button(self.master, text="Loucura pura", command=self.btnAction)
        self.button.pack(pady=self.BTN_PADDING)

        self.list_box = Listbox(self.master, width=self.WIDTH, justify="center")
        self.list_box.pack(fill="both", expand=True, padx=self.PADDING, pady=self.PADDING)

    def btnAction(self, event=None):
        search_input = self.entry.get()
        if not search_input:
            return

        if not self.queue:
            th = threading.Thread(target=self.getMp3FromYoutubeSearch, args=(search_input,))
            th.start()
        else:
            self.queue.append(search_input)

        self.entry.delete(0, 'end')


    def getMp3FromYoutubeSearch(self, search_input, video_extension="mp4"):
        self.list_box.insert('end', search_input)
        search = Search(search_input)
        first_result = search.results[0]
        title = first_result.title
        url = first_result.watch_url
        self.list_box.delete("end")
        self.list_box.insert("end", title)

        yt = YouTube(url)
        streams = yt.streams.filter(file_extension=video_extension)
        streams.first().download()

        video_path = title.replace(".", "").replace('\'','') + "." + video_extension

        try: 
            clip = VideoFileClip(video_path)
            clip.audio.write_audiofile(title + ".mp3")
            clip.close()
            self.clean_folder()
            self.list_box.delete(0)
        except Exception as e:
            clip.close()
            self.clean_folder()
            self.list_box.delete(0)
            print(e)

    def clean_folder(self):
        for filename in Path(".").glob("*.mp4"):
            os.remove(filename)
def main():
    root= Tk()
    psybot = Psybot(root)
    root.mainloop()

if __name__ == '__main__':
    main()