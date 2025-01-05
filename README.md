<table align="center">
    <tr>
        <td align="center">
            <img src="https://github.com/user-attachments/assets/6c300a6c-bed5-477e-8b7e-16ffbcd1fd4d" width="300">
        </td>
        <td></td>
        <td align="center">
            <p>Generate short videos with quotes and music effortlessly. Easily create content for platforms like Instagram, TikTok, and YouTube Shorts. This is a first basic version, mainly for personal use.
</p>
        </td>
       <td></td>
    </tr>
</table>

<br><br>

## 🌟 **Features**

- 🖋️ **Text Overlay**: Adds styled quotes and branding to videos.
- 🛠️ **Extensible Codebase**: Modular design for easy customizations.
- 🎨 **Video Effects**: Includes fade-in/out transitions and opacity-adjusted overlays.
- 🎵 **Dynamic Music Integration**: Randomly selects music, trims, and syncs with videos.
- 🔄 **Quote Management**: Automatically cycles through quotes and removes duplicates.
- ✂️ **Video Trimming & Resizing**: Ensures perfect aspect ratios for social media platforms.

---

<br><br>

## 📜 **How It Works**

| Component           | Functionality                                                                 |
|---------------------|------------------------------------------------------------------------------|
| `config.py`         | Sets up directories and default files if they don’t exist.                   |
| `main.py`           | Ties everything together for seamless video generation.                     |
| `music_manager.py`  | Randomly selects and synchronizes background music with videos.              |
| `video_processor.py`| Handles trimming, resizing, adding overlays, and applying fades to videos.   |
| `quote_manager.py`  | Manages quotes, ensures no duplicates, and cycles through them sequentially. |

---

<br><br>

## 📂 **Folder Structure**

```plaintext
├── quote_manager.py       # Manages Quotes
├── video_processor.py     # Processes Videos
├── config.py              # Base Configuration
├── main.py                # Main Application Logic
├── music_manager.py       # Handles Music Integration
├── folders/
│   ├── videos/            # Input Video Files
│   ├── musics/            # Input Music Files
│   ├── saved_videos/      # Final Output Directory
│   ├── final_video/       # Temporary Processing Directory
├── static/
    ├── Roboto-Regular.ttf # Overlay Font
    ├── Roboto-Black.ttf   # Branding Font
    ├── quotes.txt         # Contains Quotes
    ├── last.txt           # Tracks Last Quote
```

</div>
