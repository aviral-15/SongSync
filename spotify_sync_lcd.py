import re
import time
import requests
import spotipy

from spotipy.oauth2 import SpotifyOAuth

# ====================================
# CONFIG
# ====================================

ESP_IP = "IP address showing on lcd"

CLIENT_ID = "YOUR_CLIENT_ID"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"

# ====================================
# SPOTIFY
# ====================================

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri="http://127.0.0.1:8888/callback",
        scope="user-read-playback-state user-read-currently-playing"
    )
)

# ====================================
# LCD
# ====================================

def send_to_lcd(line1, line2=""):
    try:
        requests.get(
            f"http://{ESP_IP}/set",
            params={
                "line1": line1[:16],
                "line2": line2[:16]
            },
            timeout=2
        )
    except:
        pass

def center(text):
    return text.center(16)[:16]

# ====================================
# LRC PARSER
# ====================================

def parse_lrc(synced_lyrics):

    lyrics = []

    # last_spotify_check = 0
    # cached_current = None

    # last_display = ("", "")

    pattern = r"\[(\d+):(\d+\.\d+)\](.*)"

    for line in synced_lyrics.splitlines():

        match = re.match(pattern, line)

        if not match:
            continue

        mins = int(match.group(1))
        secs = float(match.group(2))

        timestamp = mins * 60 + secs

        lyric = match.group(3).strip()

        if lyric:
            lyrics.append((timestamp, lyric))

    return lyrics

# ====================================
# SPLIT TO LCD
# ====================================

def split_for_lcd(text):

    words = text.split()

    chunks = []
    current = ""

    for word in words:

        candidate = word if current == "" else current + " " + word

        if len(candidate) <= 16:
            current = candidate
        else:
            chunks.append(current)
            current = word

    if current:
        chunks.append(current)

    return chunks

def make_pages(text):

    chunks = split_for_lcd(text)

    pages = []

    for i in range(0, len(chunks), 2):

        line1 = chunks[i]

        if i + 1 < len(chunks):
            line2 = chunks[i + 1]
        else:
            line2 = ""

        pages.append((line1, line2))

    return pages
# ====================================
# GET LRCLIB
# ====================================

def get_synced_lyrics(track, artist, album, duration):

    try:

        response = requests.get(
            "https://lrclib.net/api/get",
            params={
                "track_name": track,
                "artist_name": artist,
                "album_name": album,
                "duration": duration
            },
            timeout=10
        )

        if response.status_code != 200:
            return None

        data = response.json()

        if "syncedLyrics" not in data:
            return None

        return parse_lrc(data["syncedLyrics"])

    except:
        return None

# ====================================
# MAIN LOOP
# ====================================

last_song = ""

lyrics_cache = {}

lyrics = []

last_spotify_check = 0
cached_current = None

last_display = ("", "")

while True:

    try:

        if time.time() - last_spotify_check > 0.5:

            cached_current = sp.current_playback()
            last_spotify_check = time.time()

        current = cached_current

        if not current or not current["item"]:
            time.sleep(1)
            continue

        track = current["item"]["name"]
        artist = current["item"]["artists"][0]["name"]
        album = current["item"]["album"]["name"]

        duration = round(
            current["item"]["duration_ms"] / 1000
        )

        progress = current["progress_ms"] / 1000

        song_id = current["item"]["id"]

        # SONG CHANGED

        if song_id != last_song:

            print("NEW SONG:", track)

            send_to_lcd(
                center(track[:16]),
                center(artist[:16])
            )

            time.sleep(1)

            cache_key = f"{track}|{artist}"

            if cache_key in lyrics_cache:
                lyrics = lyrics_cache[cache_key]
            else:
                lyrics = get_synced_lyrics(
                    track,
                    artist,
                    album,
                    duration
                )

                lyrics_cache[cache_key] = lyrics

            if lyrics is None:

                send_to_lcd(
                    center("No Synced"),
                    center("Lyrics")
                )

                last_song = song_id
                time.sleep(2)
                continue

            last_song = song_id

        if not lyrics:
            time.sleep(1)
            continue

        current_index = -1

        for i in range(len(lyrics)):

            timestamp, text = lyrics[i]

            if progress >= timestamp:
                current_index = i

        if current_index == -1:
            time.sleep(0.1)
            continue

        current_time = lyrics[current_index][0]
        current_line = lyrics[current_index][1]

        if current_index < len(lyrics) - 1:
            next_time = lyrics[current_index + 1][0]
        else:
            next_time = current_time + 3

        duration_available = next_time - current_time

        pages = make_pages(current_line)

        if len(pages) == 0:
            pages = [("", "")]

        page_duration = max(
            duration_available / len(pages),
            0.2
        )

        elapsed = progress - current_time

        page_index = int(elapsed / page_duration)

        if page_index >= len(pages):
            page_index = len(pages) - 1

        line1, line2 = pages[page_index]

        print(f"{current_time:.2f}s -> {line1} | {line2}")

        send_to_lcd(
            center(line1),
            center(line2)
        )

        time.sleep(0.1)

    except Exception as e:

        print("ERROR:", e)

        time.sleep(2)
