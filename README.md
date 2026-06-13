# 🎵 SongSync

A real-time Spotify lyrics display powered by **ESP8266**, **16x2 I2C LCD**, **Spotify Web API**, and **LRCLIB**.

SongSync automatically detects the song currently playing on Spotify, fetches synchronized lyrics, and displays them in real-time on a Wi-Fi connected LCD display.

---

## ✨ Features

* 🎶 Real-time synchronized lyrics
* 🔄 Automatic song change detection
* 📡 Wi-Fi communication between PC and ESP8266
* 🖥️ 16x2 LCD lyric display
* 📜 Long lyric pagination without cutting words
* ⚡ Lyrics caching for faster switching
* 🎯 Center-aligned text display
* 🌐 Powered by LRCLIB synchronized lyrics API

---

## 🏗️ System Architecture

```text
Spotify Desktop App
         │
         ▼
    Python Script
         │
         ▼
       LRCLIB
         │
         ▼
      ESP8266
         │
         ▼
    16x2 LCD Display
```

---

## 🛠️ Hardware Used

* ESP8266 NodeMCU
* 16x2 LCD Display
* I2C LCD Backpack
* USB Cable
* Wi-Fi Network

---

## 🔌 Wiring

| LCD | NodeMCU |
| --- | ------- |
| VCC | VIN     |
| GND | GND     |
| SDA | D2      |
| SCL | D1      |

---

## 📦 Software Stack

* Python
* Spotipy
* Requests
* Spotify Web API
* LRCLIB API
* ESP8266 Arduino Core

---

## 🚀 Installation

### Clone the repository

```bash
git clone https://github.com/aviral-15/SongSync.git
cd SongSync
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure Spotify Credentials

Create a Spotify Developer Application and replace:

```python
CLIENT_ID = "YOUR_CLIENT_ID"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"
```

in `spotify_sync_lcd.py`.

### Upload ESP8266 Firmware

Flash the provided ESP8266 sketch and connect the LCD using the wiring shown above.

### Run

```bash
python spotify_sync_lcd.py
```

---


## 💡 Future Improvements

* OLED/TFT display support
* Album art display
* Standalone ESP32 version
* Bluetooth support
* Mobile app integration
* Automatic startup with Windows

---

## 🤝 Contributing

Contributions, ideas, and improvements are welcome.

Feel free to open an issue or submit a pull request.

