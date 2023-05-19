import tkinter as tk
from tkinter import ttk
from pytube import *

LARGE_FONT = ('Verdana', 12)
FORMATS = ['Audio', 'Video', 'Audio and Video (Seperate)', 'Audio and Video (Combined)']
SEARCH_BUTTONS = []

def greet_user():
    """
    (None) -> None
    
    Displays a welcome message to the user.
    """
    
    fobj = open('youtube_welcome.txt')
    message = fobj.read()
    fobj.close()
    
    return message

def display_buttons(buttons):
    """
    (list) -> None
    
    Generates buttons in one column, starting at row 2.
    """
    
    for index, button in enumerate(buttons):
        button.grid(row = index+2, column = 0)

def destroy_buttons(buttons):
    """
    (list) -> None
    
    Destroys all buttons in a list of buttons.
    """
    for button in buttons:
        button.destroy()

def create_stream_info(stream):
    """
    (stream) -> str
    
    Returns a string containing information about a video download.
    """
    
    info = 'ITAG: '+str(stream.itag)+'\n'
    info += 'Bitrate: '+str(stream.abr)+'\nAudio Format: '+str(stream.audio_codec)
    info += '\nVideo Format: '+str(stream.video_codec)
    info += '\nSize: '+str(stream.filesize_approx)+' bytes'
    info += '\nResolution: '+str(stream.resolution)
    
    return info

def format_selection_window(stream):
    """
    (stream) -> None
    
    Creates a window containing buttons for each format (audio, video, split, combined) for a particular
    stream. This is used to select a download format before being able to download.
    """

    window = tk.Toplevel()
    window.title(stream.title)
    
    label = ttk.Label(window, text = 'Select your format', font = LARGE_FONT)
    label.pack(padx = 10, pady = 10)
    
    for stream_format in FORMATS:
        #Here, a variable named command is assigned a lambda function which takes button_text as a
        #parameter. button_text is then assigned the value of stream_format. Everything after the colon is what the lambda
        #function does with the parameter button_text.
        button = ttk.Button(window, text = stream_format,
                            command = lambda button_text = stream_format: [window.destroy(), download_list_window(stream, button_text)])
        button.pack()

def downloaded_stream_window():
    window = tk.Toplevel()
    label = ttk.Label(window, text = 'Stream Downloaded!', font = LARGE_FONT)
    label.pack(padx = 10, pady = 10)

        
def display_streams(streams, window):
    
    """
    (list[stream], Tk) -> None
    
    Creates a grid of buttons which display stream info and can be clicked
    to download a stream.
    """
    
    row, column = (0,0)
    
    
    for stream in streams:
        button = ttk.Button(window, text = create_stream_info(stream),
                            command = lambda k = stream: [k.download(r"PASTE DOWNLOAD PATH HERE"), window.destroy(), downloaded_stream_window()])
        if column == 9:
            column = 0
            row += 1
        button.grid(row = row, column = column)
        column += 1
    
        
def download_list_window(stream, stream_format):
    """
    (stream, str) -> None
    
    Calls the display_streams function to display download buttons for streams
    of a specific format (ie. audio, video, split, combined).
    """
    
    window = tk.Toplevel()
    window.title('Streams')
    
    label = ttk.Label(window, text = 'Streams', font = LARGE_FONT)
    label.grid(row = 0, column = 0)
    
    if stream_format == FORMATS[0]:
        streams = stream.streams.filter(only_audio = True)
    elif stream_format == FORMATS[1]:
        streams = stream.streams.filter(only_video = True)
    elif stream_format == FORMATS[2]:
        streams = stream.streams.filter(adaptive = True)
    elif stream_format == FORMATS[3]:
        streams = stream.streams.filter(progressive = True)

    display_streams(streams, window)
    

#Inherits from the tkinter Tk class
class App(tk.Tk):
    
    # *args represents any number of positional arguments
    # **kwargs represent any number of keyword arguments
    # Essentially, this just allows the class to take any number
    # of parameters when initializing.
    def __init__(self, *args, **kwargs):
        
        #Initialize Tkinter when starting app.
        tk.Tk.__init__(self, *args, **kwargs)
        
        #Define frame named page_container which will contain all the pages in the app. Elements in the page_container
        #are accesible on any page in the app (ie. logo, app name, and QUIT button).
        
        #This page container has App as the page_container widget.
        page_container = tk.Frame(self)
        page_container.pack(side = 'top', fill = 'both', expand = True)
        tk.Tk.wm_title(self, 'YouTube Downloader')
        tk.Tk.iconbitmap(self, default = 'youtube_logo_Dll_icon.ico')
        
        page_container.grid_rowconfigure(0, weight = 1)
        page_container.grid_columnconfigure(0, weight = 1)
        
        quit_button = ttk.Button(text = 'QUIT', command = page_container.quit)
        quit_button.pack(side = 'bottom')
        
        #Create a dictionary containing the frames.
        self.frames = {}
        
        #Iterate through the tuple of frames and add them to the dictionary
        #of frames (self.frames)
        for F in (StartPage, IntroPage, ModeSelect, YouTubeSearch, UrlSearch):
            
            #Creates frames where their page_container is the page_container, and their
            #main_app is App (self = App).
            frame = F(page_container, self)
            
            self.frames[F] = frame
            
            frame.grid(row = 0, column = 0, sticky = 'nsew')
        
        #Start by bringing StartPage to the top.
        self.show_frame(StartPage)
        
    
    def show_frame(self, frame_key):
        """
        (tk.Frame) -> None
        
        Raises a frame to the top to be displayed.
        """
        frame = self.frames[frame_key]
        frame.tkraise()


#The following classes are pages inside of App (referred to as main_app). This code
#can be confusing because it seems that these pages are never assigned to a variable,
#so they seemingly are never displayed. In reality, they are created when creating the page
#dictionary in App.
        

class StartPage(tk.Frame):
    
    def __init__(self, page_container, main_app):
        
        #Initializes frame inside of page_container (ie. page container is the parent frame).
        tk.Frame.__init__(self, page_container)
        
        label = ttk.Label(self, text = 'YouTube Downloader by Jikael Gagnon', font = LARGE_FONT)
        label.pack(padx = 10, pady = 10)
        
        intro_button = ttk.Button(self, text = 'First Time? Click Here!', command = lambda : main_app.show_frame(IntroPage))
        intro_button.pack()
        
        start_button = ttk.Button(self, text = 'Start', command = lambda : main_app.show_frame(ModeSelect))
        start_button.pack()

class IntroPage(tk.Frame):
    
    def __init__(self, page_container, main_app):
        tk.Frame.__init__(self,page_container)
        
        welcome = ttk.Label(self, text = 'Welcome to the YouTube Downloader!', font = LARGE_FONT)
        welcome.pack(padx = 10, pady = 10)
        
        info = ttk.Label(self, text = greet_user())
        info.pack(padx = 10, pady = 10)
        
        start_button = ttk.Button(self, text = 'Start', command = lambda : main_app.show_frame(ModeSelect))
        start_button.pack()
        
        home_button = ttk.Button(self, text = 'Back to Home', command = lambda : main_app.show_frame(StartPage))
        home_button.pack()
        

class ModeSelect(tk.Frame):
    
    def __init__(self, page_container, main_app):
        tk.Frame.__init__(self,page_container)
        
        label = ttk.Label(self, text = 'How would you like to search for a video?', font = LARGE_FONT)
        label.pack(padx = 10, pady = 10)
        
        search_youtube_button = ttk.Button(self, text = 'Search YouTube', command = lambda : main_app.show_frame(YouTubeSearch))
        search_youtube_button.pack()
        
        search_url_button = ttk.Button(self, text = 'Enter URL', command = lambda : main_app.show_frame(UrlSearch))
        search_url_button.pack()
        
        home_button = ttk.Button(self, text = 'Back to Home', command = lambda : main_app.show_frame(StartPage))
        home_button.pack()
        
class YouTubeSearch(tk.Frame):
    
    def __init__(self, page_container, main_app):
        tk.Frame.__init__(self,page_container)
        
        label = ttk.Label(self, text = 'YouTube Search', font = LARGE_FONT)
        label.grid(row = 0, column = 0)
             
        text = tk.StringVar()
        searchbar = ttk.Entry(self, textvariable = text)
        searchbar.grid(row = 1, column = 0)
        
        self.results_buttons("")
        
        search_button = ttk.Button(self, text = 'Search', command = lambda : [destroy_buttons(BUTTONS), self.results_buttons(text.get()), display_buttons(BUTTONS)])
        search_button.grid(row = 1, column = 1)
        
        mode_select_button = ttk.Button(self, text = 'Back to Mode Selection', command = lambda : main_app.show_frame(ModeSelect))
        mode_select_button .grid(row = 1, column = 3)
        
        home_button = ttk.Button(self, text = 'Back to Home', command = lambda : main_app.show_frame(StartPage))
        home_button.grid(row = 1, column = 4)
        
    def results_buttons(self, text):
        search = Search(text)
        
        global BUTTONS
        
        BUTTONS = []
        
        for stream in search.results:
            button = ttk.Button(self, text = stream.title, command = lambda k = stream: format_selection_window(k))
            BUTTONS.append(button)
            
        
        
class UrlSearch(tk.Frame):
    
    def __init__(self, page_container, main_app):
        tk.Frame.__init__(self,page_container)
        
        text = tk.StringVar()
        searchbar = ttk.Entry(self, textvariable = text)
        searchbar.grid(row = 1, column = 0)
        
        label = ttk.Label(self, text = 'URL Search', font = LARGE_FONT)
        label.grid(row = 0, column = 0)
        
        download_options_button = ttk.Button(self, text = 'Search', command = lambda : format_selection_window(YouTube(text.get())))
        download_options_button.grid(row = 1, column = 1)
        
        mode_select_button = ttk.Button(self, text = 'Back to Mode Selection', command = lambda : main_app.show_frame(ModeSelect))
        mode_select_button.grid(row = 1, column = 3)
        
        home_button = ttk.Button(self, text = 'Back to Home', command = lambda : main_app.show_frame(StartPage))
        home_button.grid(row = 1, column = 4)
        
        
        
# -- TODO: Modular Stream Page --

# class VideoPage(tk.Frame):
#     
#     def __init__(self, page_container, main_app):
#         tk.Frame.__init__(self,page_container)
#         
#         text = tk.StringVar()
#         button_1 = ttk.Button(self, text = 'Audio')
#         button_1.pack()
#         
    
               
app = App()

app.mainloop()
app.destroy()
