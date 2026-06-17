# SpotMusic 🎵

SpotMusic is a graphical user interface (GUI) desktop application built with Python that allows you to seamlessly download your favorite Spotify songs and playlists as MP3 files. 

The application works by retrieving track metadata (Title and Artist) directly from Spotify and then securely searching and downloading the highest quality audio counterpart from YouTube using `yt-dlp`.

## ✨ Features

* **Spotify Integration:** Securely log in to your Spotify account to fetch your private, public, and collaborative playlists.
* **Single Track Download:** Paste a Spotify track link to download a specific song.
* **Full Playlist Download:** Select any of your saved playlists and download all tracks with a single click.
* **Custom Download Location:** Choose exactly where you want your audio files saved.
* **Modern UI:** Built using `customtkinter` for a sleek, modern, dark-mode graphical interface.
* **Background Processing:** Downloads run asynchronously via threading, ensuring the app remains responsive while downloading.

## 🛠️ Prerequisites

Before running the application, ensure you have the following installed on your system:

1. **Python 3.8+**
2. **FFmpeg:** This is **strictly required** by `yt-dlp` to extract and convert the downloaded media into MP3 format. 
   * Download FFmpeg from [the official website](https://ffmpeg.org/download.html).
   * Extract it and ensure the `bin` folder is added to your system's Environment Variables (`PATH`).

## 📦 Installation

1. **Clone the repository or download the source code.**
2. **Install the required Python dependencies:**
   Open your terminal/command prompt and run:
   ```bash
   pip install customtkinter spotipy python-dotenv yt-dlp youtube-search-python requests pillow


## ⚙️ Configuration (Spotify API Setup)
To allow the app to access Spotify data, you need to set up a Spotify Developer Application.

Go to the Spotify Developer Dashboard.

Log in with your Spotify account and click Create App.

Fill in the required details (App name, description).

In the app settings, set the Redirect URI to http://localhost:8888/callback (or any custom local URI you prefer).

Copy your Client ID and Client Secret.

Create a file named .env in the same directory as SpotMusic.py and populate it with your credentials:

## .env File 
```text
CLIENT_ID=your_spotify_client_id_here
CLIENT_SECRET=your_spotify_client_secret_here
REDIRECT_URI=http://localhost:8888/callback
Make the .env file and store your credentials inside it.
```

## 🚀 Usage
Run the application using Python:

```bash
python SpotMusic.py
```

## Navigating the App:
Set Download Folder: Click "Set Your Folder" to choose where downloaded MP3s will be saved. The app remembers this location.

Download via Link: Paste a direct Spotify Track URL into the input field and click "Download this song".

Download from Playlists: 1. Click "Login With Your Spotify Account" (this will open your browser for authorization).
2. Once logged in, click "Download Songs from Your Playlist".
3. Select a playlist from the dropdown menu to view its cover art and tracks.
4. You can either select a specific song to download or click "Download Full Playlist".

## 📂 App Data Storage
The application creates a configuration folder to store your download path preferences and cache your Spotify login token. On Windows, this is typically located at:
%APPDATA%/SpotMusic/data

## ⚠️ Disclaimer
This tool is created for educational and personal use only. Downloading copyrighted material without permission may violate the terms of service of the respective platforms (Spotify and YouTube). The creator assumes no responsibility for how this tool is used.
"""