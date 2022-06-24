from pytube import YouTube, Search
from moviepy.editor import VideoFileClip
import os
from tkinter import Tk, Label, Entry, Button, Listbox
from collections import deque
import threading

class Psybot:
    def __init__(self, master):
        master.title("Psybot")
        self.master = master

        self.queue = deque()

        self.set_ui()

        self.master.bind('<Return>', self.btnAction)

    def set_ui(self):
        self.intro_lbl = Label(self.master, text="ATENÇÃO! USE APENAS PARA PSYTRANCE")
        self.intro_lbl.pack()

        self.entry = Entry(self.master)
        self.entry.pack()

        self.button = Button(self.master, text="Loucura pura", command=self.btnAction)
        self.button.pack()

        self.list_box = Listbox(self.master)
        self.list_box.pack()

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
            os.remove(video_path)
            self.list_box.delete(0)
        except Exception as e:
            os.remove(video_path)
            self.list_box.delete(0)
            print(e)

def main():
    root= Tk()
    psybot = Psybot(root)
    root.mainloop()

if __name__ == '__main__':
    main()