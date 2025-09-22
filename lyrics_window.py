import argparse
import os
import sys
import time
import threading
from typing import Optional, List

# Use Tkinter for the lyrics window
try:
    import tkinter as tk
except Exception as e:
    print("Tkinter is required to display lyrics window.")
    raise

# Audio playback is optional; requires pygame installed
try:
    import pygame
    _HAS_PYGAME = True
except Exception:
    _HAS_PYGAME = False


def read_lyrics(path: Optional[str]) -> List[str]:
    if path and os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                text = f.read()
        except UnicodeDecodeError:
            with open(path, 'r', encoding='latin-1') as f:
                text = f.read()
        lines = [ln.strip() for ln in text.splitlines()]
        return [ln for ln in lines if ln != ""] or ["(Lyrics file is empty)"]
    # Default sample lyrics
    return [
        "You crashed into me, now hear this rhyme,",
        "In a separate window, one line at a time.",
        "Add your song in assets, name it song.mp3,",
        "And put your lyrics in lyrics.txt for free!",
    ]


def play_audio(audio_path: str):
    if not audio_path or not os.path.exists(audio_path):
        return
    try:
        if not _HAS_PYGAME:
            print("pygame not installed; skipping audio playback.")
            return
        pygame.mixer.init()
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play()
    except Exception as e:
        print(f"Audio play failed: {e}")


def run_lyrics_window(lyrics_path: str | None, audio_path: str | None, interval: float, title: str):
    lines = read_lyrics(lyrics_path)

    # Start audio in background if provided
    if audio_path:
        threading.Thread(target=play_audio, args=(audio_path,), daemon=True).start()

    root = tk.Tk()
    root.title(title)
    root.geometry("640x360")

    # Widgets
    frame = tk.Frame(root, bg="#111")
    frame.pack(fill=tk.BOTH, expand=True)

    label = tk.Label(frame, text="", font=("Segoe UI", 20, "bold"), fg="#f0f0f0", bg="#111", wraplength=600, justify=tk.CENTER)
    label.pack(pady=40)

    controls = tk.Frame(frame, bg="#111")
    controls.pack(side=tk.BOTTOM, pady=10)

    close_btn = tk.Button(controls, text="Close", command=root.destroy)
    close_btn.pack()

    idx = {"i": 0}

    def show_next():
        i = idx["i"]
        if i < len(lines):
            label.config(text=lines[i])
            idx["i"] = i + 1
            root.after(int(interval * 1000), show_next)
        else:
            # Leave last line on screen; optionally auto-close after a delay
            pass

    # Start sequence
    root.after(200, show_next)

    try:
        root.mainloop()
    finally:
        # Stop audio when window closes
        if _HAS_PYGAME:
            try:
                import pygame
                pygame.mixer.music.stop()
                pygame.mixer.quit()
            except Exception:
                pass


def parse_args(argv: list[str]):
    p = argparse.ArgumentParser(description="Display lyrics line-by-line in a window.")
    p.add_argument('--lyrics', type=str, default=None, help='Path to lyrics text file (UTF-8).')
    p.add_argument('--audio', type=str, default=None, help='Optional path to song file (mp3/wav).')
    p.add_argument('--interval', type=float, default=1.5, help='Seconds between lines.')
    p.add_argument('--title', type=str, default='Lyrics', help='Window title.')
    return p.parse_args(argv)


if __name__ == '__main__':
    args = parse_args(sys.argv[1:])
    run_lyrics_window(args.lyrics, args.audio, args.interval, args.title)
