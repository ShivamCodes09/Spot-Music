import PIL.Image
import PIL.ImageShow
import customtkinter 
from customtkinter import CTkButton,CTkLabel,CTkEntry,CTkFrame,CTkOptionMenu,CTkImage,CTkProgressBar,CTkTabview
import os
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
import yt_dlp
from yt_dlp import YoutubeDL
import os
from tkinter import messagebox,OptionMenu,filedialog
from youtubesearchpython import searchYoutube
import multiprocessing
from spotipy import SpotifyOAuth,Spotify
import requests
import PIL 
import threading
import sys
import multiprocessing 

# creating a folder in APPDATA
app_path=os.getenv("APPDATA")
app_folder="SpotMusic"
config_folder=os.path.join(app_path,app_folder)

if not os.path.exists(config_folder):
    os.makedirs(f"{config_folder}/data")
    open(f"{config_folder}/data/path.txt","w")
user=os.path.expanduser("~")
default_path=os.path.join(user,"Downloads")
new_path=None
actual_path=[]
try:
    with open(f"{config_folder}/data/path.txt","r") as h:
        pt=h.read()
        if pt:
            actual_path.append(pt)
        else:
            with open(f"{config_folder}/data/path.txt","w") as h:
                h.write(default_path)
                actual_path.append(default_path)
except FileNotFoundError:
    with open(f"{config_folder}/data/path.txt","w") as h:
        h.write(default_path)
        actual_path.append(default_path)

# For Pyinstaller 
def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Loading API Key,Client Id,Redirect URI
load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI=os.getenv("REDIRECT_URI")

# outh
sp_oauth = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope="user-library-read playlist-read-private playlist-read-collaborative",
    )
def get_auth_header(token):
    return {"Authorization": "Bearer " + token}
Access_token=[]
token_info=sp_oauth.get_cached_token()
if token_info:
    Access_token.append(token_info['access_token'])


sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID,
                                                           client_secret=CLIENT_SECRET))
try:
    user=sp.me()
    username=user['display_name']
except:
    pass


playlist={}
playlist_images={}
playlist_name=[]
songs={}
current_song=[]
playlist_track=[]
song_artist={}
currentsong_link=[]
def get_user_playlist(token):
    headers=get_auth_header(token)
    response = requests.get("https://api.spotify.com/v1/me/playlists", headers=headers)
    response_json=response.json()
    for item in response_json["items"]:
        print(item['images'][0]['url'])
        playlist[item["name"]]=item["id"]
        playlist_images[item['name']]=item['images'][0]['url']
        playlist_name.append(item["name"])

def get_playlist_track(token,playlist_id):
    result=sp.playlist(playlist_id)
    current_song.clear()
    currentsong_link.clear()
    for track_data in result['tracks']['items']:
        track=track_data['track']
        song_name=track['name']
        artist_name=track['artists'][0]['name']
        song_link=track['external_urls']['spotify']
        playlist_track.append(song_name)
        songs[song_name]=song_link
        song_artist[song_name]=artist_name
        current_song.append(song_name)
        currentsong_link.append(song_link)

# Folder
def set_folder():
    folder_path=filedialog.askdirectory()
    if folder_path:
        with open(resource_path(f"{app_path}\\MsDelta\\data\\path.txt"),"w") as t:
            t.write(folder_path)
            actual_path.clear()
            actual_path.append(folder_path) 
            d_path.configure(text=f"Your File will be saved in {actual_path[0]}")

def path_viewer():
    with open(f"{config_folder}/data/path.txt","r") as h:
        pt=h.read()
        if pt:
            return pt
        else:
            return default_path


label5=None
bt4=None
def logout():
    global bt4
    global bt3
    l=os.listdir()
    if ".cache" in l:
        per=messagebox.askyesno(title="Logout?",message="ARE YOU SURE?")
        if per:
            os.remove('.cache')
            Access_token.clear()
            if not label5==None:
                label5.destroy()
            label3.destroy()
            bt3=CTkButton(frame1,text="""Login With Your 
    Spotify Account""",command=thread_login,height=50)
            bt3.place(relx=0.75,rely=0.26)
            messagebox.showinfo("Done","Logout Succesfully") 
    else:
        messagebox.showinfo("Done","Please login first")

def down_link():
    try:
        a=threading.Thread(target=download).start()
    except RuntimeError:
        messagebox.showinfo("Oops","Already Started Downloading!")

down_bt=None
def song_choice(choice):
    global down_bt
    if not down_bt==None:
        down_bt.destroy()
    link=songs[choice]
    down_bt=CTkButton(frame2,text=f"Download {choice}",command=threading.Thread(target=download,args=(link,None)).start)
    down_bt.place(relx=0.6,rely=0.4)


def download_images(link,name):
    response=requests.get(link)
    with open(resource_path(f"{config_folder}/data/{name}.png"),'wb') as down:
        down.write(response.content)
img=None
menu=None
def show(choice):
    global img
    global menu
    global down_bt
    if not img==None:
        img.destroy() 
    if not menu==None:
        menu.destroy()
    if not down_bt==None:
        down_bt.destroy() 
    print(choice)
    id=playlist[choice]
    get_playlist_track(Access_token[0],id)
    link=playlist_images[choice]
    download_images(link,choice)
    image=PIL.Image.open(resource_path(f"{config_folder}/data/{choice}.png"))
    i=CTkImage(light_image=image,dark_image=image,size=(250,250))
    img=CTkLabel(frame2,text="",image=i)
    os.remove(resource_path(f"{config_folder}/data/{choice}.png"))
    img.place(relx=0.1,rely=0.2)
    menu=CTkOptionMenu(frame2,values=current_song,command=song_choice)
    menu.set("Select a Song")
    menu.place(relx=0.15,rely=0.67)
    down_pl=CTkButton(frame2,text="Download Full Playlist",command=threading.Thread(target=download,args=(None,currentsong_link)).start)
    down_pl.place(relx=0.6,rely=0.3)
    

def f2():
    if not Access_token:
        messagebox.showerror("Error","Please Login with Your Spotify Account.")
    else:
        for i in frame2.winfo_children():
            i.destroy()
        frame1.pack_forget()
        frame2.pack(fill="both",expand=True)
        frame2.tkraise()
        frame2.pack_propagate(False)
        get_user_playlist(Access_token[0])
        l=[i for i in playlist.keys()]
        option=CTkOptionMenu(frame2,values=l,command=show)
        option.set("Your Playlist")
        option.pack(pady=20)
        back_bt=CTkButton(frame2,text="Back To Homepage",command=lambda:mscreen())
        back_bt.place(relx=0.1,rely=0.033)
        folder=CTkButton(frame2,text="Set Your Folder",command=set_folder)
        folder.place(relx=0.7,rely=0.033)
        pass

def Login():
    global label5
    if not Access_token:
        code=sp_oauth.get_authorization_code()
        token=sp_oauth.get_access_token(code)
        print(type(token),token)
        Access_token.append(token['access_token'])
        user=sp.me()
        username=user['display_name']
        label5=CTkLabel(frame1,text=f"Welcome {username}")
        label5.place(relx=0.77,rely=0.1)
        bt3.destroy()
        bt4=CTkButton(frame1,text="Logout",command=logout)
        bt4.place(relx=0.75,rely=0.26)
        
    else:
        messagebox.showinfo("Logged In","Already Logged IN")


def download(lnk=None,lst=None):
    try:
        down_path=path_viewer()
        global link
        if not lnk==None:
            spotify_link=lnk
        else:
            spotify_link=link.get()

        if lst:
            for i in lst:
                spotify_link=i    
                try:
                    track_id = spotify_link.split('/')[-1].split('?')[0]
                    track = sp.track(track_id)
                    title = track['name']
                    artist = track['artists'][0]['name']
                    print(f"Spotify Info: Title - {title}, Artist - {artist}")
                except Exception as e:
                    print(f"Error getting info from Spotify: {e}")
                a=searchYoutube(f"{title} {artist}",mode='dict',max_results=1)
                l=a.result()
                yt_link=l['search_result'][0]['link']

                ydl_opts = {
                            'format': 'bestaudio/best',
                            'outtmpl': f'{down_path}/%(title)s.%(ext)s',
                            'postprocessors': [{
                                'key': 'FFmpegExtractAudio',
                                'preferredcodec': 'mp3',
                                'preferredquality': '192',
                            }],
                            'noplaylist': True
                        }

                with YoutubeDL(ydl_opts) as ydl:
                    messagebox.showinfo("song",f"{title} will be downloaded in few minutes")
                    ydl.download([yt_link])
                    messagebox.showinfo("Download Succesfully","Dowloaded successfully")
        else:
            try:
                track_id = spotify_link.split('/')[-1].split('?')[0]
                track = sp.track(track_id)
                title = track['name']
                artist = track['artists'][0]['name']
                print(f"Spotify Info: Title - {title}, Artist - {artist}")
            except Exception as e:
                print(f"Error getting info from Spotify: {e}")
            a=searchYoutube(f"{title} {artist}",mode='dict',max_results=1)
            l=a.result()
            yt_link=l['search_result'][0]['link']


            ydl_opts = {
                        'format': 'bestaudio/best',
                        'outtmpl': f'{down_path}/%(title)s.%(ext)s',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }],
                        'noplaylist': True
                    }

            with YoutubeDL(ydl_opts) as ydl:
                messagebox.showinfo("song",f"{title} will be downloaded in few minutes")
                ydl.download([yt_link])
                messagebox.showinfo("Download Succesfully","Dowloaded successfully")
    except Exception as e:
        messagebox.showinfo("error",f"Please Enter correct Data i.e {e}")    
def thread_login():
        threading.Thread(target=Login).start()

def mscreen():
    global link
    global bt3
    global bt4
    global label3
    global d_path
    for i in frame1.winfo_children():
        i.destroy()
    frame2.pack_forget()
    frame1.pack(fill="both",expand=True)
    frame2.pack_propagate(False)
    frame1.tkraise()

    l1=CTkLabel(frame1,text="Welcome to the the downloader:")
    l1.pack(pady=20)
    link=CTkEntry(frame1,placeholder_text="Enter the link of the song:",width=250,height=75)
    link.pack(pady=20)
    bt1=CTkButton(master=frame1,text="Download this song",command=down_link)
    bt1.pack(pady=20)
    bt2=CTkButton(frame1,text="""Download Songs from 
    Your Playlist""",command=f2,height=50)
    bt2.place(relx=0.04,rely=0.26)
    bt3=CTkButton(frame1,text="""Login With Your 
    Spotify Account""",command=thread_login,height=50)
    bt3.place(relx=0.75,rely=0.26)
    label3=CTkLabel(frame1,text="")
    label3.place(relx=0.77,rely=0.1)
    fd=CTkButton(frame1,text="Set Your Folder",command=set_folder)
    fd.pack(pady=20)
    d_path=CTkLabel(frame1,text=f"Your Audio will be saved in {actual_path[0]}")
    d_path.pack(pady=20)

    if Access_token:
        global bt4
        bt3.destroy()
        bt4=CTkButton(frame1,text="Logout",command=logout)
        bt4.place(relx=0.75,rely=0.26)
        user=sp.me()
        username=user['display_name']
        label3=CTkLabel(frame1,text=f"Welcome,{username}")
        label3.place(relx=0.77,rely=0.1)

if (__name__)=="__main__":
    win=customtkinter.CTk()
    win.title("SpotMusic")
    win.geometry("700x600")
    win.iconbitmap("Icon.ico")
    frame1=CTkFrame(win,700,600)
    frame2=CTkFrame(win,700,600)
    mscreen()
    win.mainloop()
