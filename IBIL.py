from faster_whisper import WhisperModel
import sounddevice as sd
import numpy as np
from scipy.signal import resample_poly
import pyautogui
import subprocess
import webbrowser
import time

# WHISPER SETUP 

whisper_model = WhisperModel(
    "small.en",
    device="cpu",
    compute_type="int8"
)

MIC_DEVICE = 14
JBL_RATE = 48000
WHISPER_RATE = 16000


#  ACTION FUNCTIONS

def open_chrome():
    print("Opening Chrome...")
    try:
        subprocess.Popen([r"C:\Program Files\Google\Chrome\Application\chrome.exe"])
    except FileNotFoundError:
        # fallback if Chrome isn't at that path
        subprocess.Popen(['chrome.exe'])
    time.sleep(2)  # give it a moment to open

def search_chrome(query):
    print(f"Searching for: {query}")
    webbrowser.open(f"https://www.google.com/search?q={query}")

def move_arrow(direction, steps=10):
    if direction == "up" :
        pyautogui.moveRel(0, -steps, duration=0.3)
    elif direction == "down":
        pyautogui.moveRel(0, steps, duration=0.3)
    elif direction == "left":
        pyautogui.moveRel(-steps, 0, duration=0.3)
    elif direction == "right":
        pyautogui.moveRel(steps, 0, duration=0.3)
      
def take_screenshot():
    import os
    from datetime import datetime
    SCREENSHOT_DIR = r"C:\Users\DELL\Downloads\Projects\test screenshots"
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    filepath = os.path.join(SCREENSHOT_DIR, filename)
    pyautogui.screenshot(filepath)
    print(f"Screenshot saved to: {filepath}")

def open_notepad():
    print("opening notepad...")
    try:
        subprocess.Popen([r"C:\Windows\notepad.exe"])
    except: 
        subprocess.Popen(['notepad.exe'])
        time.sleep(2)

def type_notepad(text_to_type):
    print(f"typing :{text_to_type}")
    pyautogui.write(f"{text_to_type}")

    
# COMMAND INTERPRETER 

def handle_command(text):
    text = text.lower().strip()

    if "open chrome" in text:
        open_chrome()
        

    elif "search" in text:
        query = text.split("search", 1)[1].strip()
        if query:
            search_chrome(query)
        else:
            print("Didn't catch what to search for.")

    
    elif "arrow" in text :
         if "up" in text:
            move_arrow("up")
         elif "down" in text:
            move_arrow("down")
         elif "right" in text:
            move_arrow("right")
         elif "left" in text:
            move_arrow("left")
         else:
            print("say that again...")

    elif "screenshot" in text:
        take_screenshot()

    elif "notepad" in text :
        open_notepad()

    elif "type" in text:
        type_to_text = text.split("type", 1)[1].strip()
        if type_to_text : 
            type_notepad(" " + type_to_text)
        else:
           print("didnt got what you want to type") 
 
    
    elif "exit" in text or "quit" in text or "stop listening" in text:
        print("Shutting down. Bye!")
        return False  # signals the main loop to stop

    else:
        print("Sorry, I didn't understand that command.")

    return True  # keep listening

# SPEECH LOOP 

def listen_and_transcribe():
    try:
        print(" Listening...")

        duration = 5

        audio = sd.rec(
            int(duration * JBL_RATE),
            samplerate=JBL_RATE,
            channels=1,
            dtype="float32",
            device=MIC_DEVICE
        )

        sd.wait()

        print("Thinking...")

        audio = np.squeeze(audio)

        # JBL: 48 kHz → Whisper: 16 kHz
        audio_16k = resample_poly(
            audio,
            WHISPER_RATE,
            JBL_RATE
        ).astype(np.float32)

        segments, info = whisper_model.transcribe(
            audio_16k,
            language="en",
            beam_size=5
        )

        text = ""

        for segment in segments:
            text += segment.text

        text = text.strip()

        print("You said:", text)

        return text

    except Exception as e:
        print("Speech recognition error:", e)
        return None

def main():
    print("IBIL is ready. Say a command (say 'exit' to quit).")

    keep_running = True

    while keep_running:
        text = listen_and_transcribe()

        if text:
            keep_running = handle_command(text)

if __name__ == "__main__":
    main()