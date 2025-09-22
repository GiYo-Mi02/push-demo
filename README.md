# Relapse Racing (Python + Pygame)

A tiny top-down racing prototype built with Pygame. When your car crashes into an enemy car, a separate lyrics window opens and displays lines one by one. Optionally, it can play an audio file while showing the lyrics.

## Features

- Simple left/right movement and enemy spawn
- Collision detection triggers a separate lyrics window
- Lyrics window built with Tkinter (ships with Python on Windows)
- Optional audio playback using pygame.mixer (mp3/wav)

## Requirements

- Python 3.8+
- Windows (tested), should also work on macOS/Linux

## Setup (Windows)

1. Open a terminal in this folder.
2. Install dependencies:

```
pip install -r requirements.txt
```

3. (Optional) Put your song at `assets/song.mp3` and edit/add lyrics in `lyrics.txt`.

## Run

```
python main.py
```

Controls:

- Left/Right arrows or A/D to move
- ESC to quit
- R to restart after a crash

When you crash, a new window titled "Crash Lyrics" opens and displays the lyrics. If `assets/song.mp3` exists, it will play automatically.

## Customize

- Change the lyrics file path in `lyrics.txt`, or pass a different file by modifying `spawn_lyrics_window` call in `main.py`.
- Replace `assets/song.mp3` with your own audio file. Formats supported depend on SDL_mixer/pygame (mp3, wav, ogg typically work).
- Adjust the display speed by tuning the `interval_sec` argument (default 1.2s) in `main.py`.

## Troubleshooting

- If the lyrics window does not appear: check the terminal for errors, ensure Python can import `tkinter`.
- If audio does not play: ensure `pygame` installed correctly and the file exists at `assets/song.mp3`. The app will continue without sound if playback fails.
- For fonts, the code uses the default system font via `pygame.font.SysFont(None, size)`. If text looks odd, you can load a TTF font explicitly.

## Notes

- This is a minimal educational sample; feel free to expand the gameplay, add images, and polish UI.
