# IBIL-Intelligent-Bot-In-Laptop
A voice assistant made using Python and Faster-Whisper, no API required, runs on your PC. 
It uses [Faster-Whisper](https://github.com/SYSTRAN/faster-whisper) for speech recognition, so everything runs **locally on your CPU**, with no cloud API and no internet needed for transcription.

## Features

- Open Chrome and search Google by voice
- Move the mouse cursor up, down, left, or right
- Take screenshots and save them automatically
- Open Notepad and type dictated text
- 100% offline speech recognition (Whisper `small.en`, int8 on CPU)

## Voice Commands

| Say this | What happens |
|---|---|
| "open chrome" | Launches Google Chrome |
| "search *your query*" | Searches Google for your query |
| "arrow up / down / left / right" | Moves the cursor 10 pixels in that direction |
| "screenshot" | Saves a screenshot to your screenshot folder |
| "notepad" | Opens Notepad |
| "type *your text*" | Types the text wherever your cursor is focused |
| "exit", "quit", or "stop listening" | Shuts the assistant down |

**Example:** say *"search best python tutorials"* and Chrome opens with the Google results.

## Requirements

- Windows 10/11
- Python 3.9 or newer
- A working microphone
- Google Chrome (optional, only needed for the Chrome commands)

## Installation

**1. Clone the repository**

```bash
git clone https://github.com/<your-username>/IBIL-Intelligent-Bot-In-Laptop.git
cd IBIL-Intelligent-Bot-In-Laptop
```

**2. (Recommended) Create a virtual environment**

it is highly recommended that you create a virtual environment .

**3. Install the dependencies**

```bash
pip install faster-whisper sounddevice numpy scipy pyautogui
```

OR,

```bash
pip install -r requirements.txt
```

> The first time you run the program, Faster-Whisper will download the `small.en` model (a few hundred MB). After that it works fully offline.

## Setup

### 1. Find your microphone device ID

The code uses `MIC_DEVICE = 14`, which is specific to the original machine. Find your own device ID by running:

```bash
python -c "import sounddevice as sd; print(sd.query_devices())"
```

Look for your microphone in the list and note its index number.

### 2. Update the settings in the script

Open the script and edit these values near the top:

```python
MIC_DEVICE = 14        # change to your microphone's device ID
JBL_RATE = 48000       # change to your mic's sample rate (commonly 44100 or 48000)
```

### 3. Set your screenshot folder

In the `take_screenshot()` function, change this path to a folder on your computer:

```python
SCREENSHOT_DIR = r"C:\Users\DELL\Downloads\Projects\test screenshots"
```

all the screenshots taken ,using the voice command, will be saved in this folder. 


### 4. Check the Chrome path 

If Chrome is installed somewhere else, update the path in `open_chrome()`:

```python
r"C:\Program Files\Google\Chrome\Application\chrome.exe"
```

## Usage

Run the assistant:

```bash
python IBIL.py
```

*(Replace `IBIL.py` with whatever your script file is named.)*

You will see:

```
IBIL is ready. Say a command (say 'exit' to quit).
 Listening...
```

Speak your command within the 5-second recording window. The assistant transcribes it, prints what it heard, and runs the action.

## How It Works

1. Records 5 seconds of audio from your microphone
2. Resamples it from the mic's sample rate (48 kHz) to 16 kHz, which is what Whisper expects
3. Transcribes the audio locally with Faster-Whisper
4. Matches keywords in the text to a command and runs it using `subprocess`, `webbrowser`, and `pyautogui`
5. Loops back and listens again until you say "exit"

## Tech Stack

- [Faster-Whisper](https://github.com/SYSTRAN/faster-whisper): speech-to-text
- [sounddevice](https://python-sounddevice.readthedocs.io/): microphone input
- [NumPy](https://numpy.org/) and [SciPy](https://scipy.org/): audio processing and resampling
- [PyAutoGUI](https://pyautogui.readthedocs.io/): mouse movement, typing, and screenshots

## Known Limitations

- Windows only (uses Windows file paths for Chrome and Notepad)
- Fixed 5-second listening window per command
- Commands are matched by keywords, so phrasing matters
- Accuracy depends on your microphone and background noise

## Troubleshooting

| Problem | Fix |
|---|---|
| `Speech recognition error` on startup | Your `MIC_DEVICE` ID is probably wrong. Re-run `sd.query_devices()` |
| Audio sounds fast or garbled | Set `JBL_RATE` to match your mic's actual sample rate |
| Chrome doesn't open | Update the Chrome path in `open_chrome()` |
| Wrong words transcribed | Speak closer to the mic, or try a bigger model such as `medium.en` |

## Ideas for Future Improvements

- Wake word detection (e.g. "Hey IBIL")
- Continuous listening instead of fixed 5-second chunks
- Config file for paths and mic settings
- More commands (volume control, opening other apps, closing windows)

##License

This project is licensed under the MIT License. Add a LICENSE file to your repo if you want to use this.

---

Feel free to open an issue or submit a pull request if you have ideas to improve the project!
