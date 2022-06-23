from pytube import YouTube, Search
import moviepy.editor as mp
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
        self.introLbl = Label(self.master, text="ATENÇÃO!! APENAS USE PARA PSYTRANCE")
        self.introLbl.pack()

        self.entry = Entry(self.master)
        self.entry.pack()

        self.button = Button(self.master, text="Loucura pura", command=self.btnAction)
        self.button.pack()

        self.listBox = Listbox(self.master)
        self.listBox.pack()

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
        self.listBox.insert('end', search_input)
        search = Search(search_input)
        first_result = search.results[0]
        title = first_result.title
        url = first_result.watch_url
        self.listBox.delete("end")
        self.listBox.insert("end", title)

        yt = YouTube(url)
        streams = yt.streams.filter(file_extension=video_extension)
        streams.first().download()

        video_path = title.replace(".", "") + "." + video_extension

        try: 
            clip = mp.VideoFileClip(video_path)
            clip.audio.write_audiofile("doidera/" + title + ".mp3")
            os.remove(video_path)
            self.listBox.delete(0)
        except Exception as e:
            os.remove(video_path)
            self.listBox.delete(0)
            print(e)

if __name__ == "__main__":
    root= Tk()
    psybot = Psybot(root)
    root.mainloop()