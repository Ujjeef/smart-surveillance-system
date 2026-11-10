import os
import sys
import threading
import subprocess
import platform

import numpy as np
import wave

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import BASE_DIR

SIREN_PATH = os.path.join(BASE_DIR, "sounds", "siren.wav")
SAMPLE_RATE = 44100


class SirenPlayer:
    def __init__(self, sound_path=SIREN_PATH):
        self.sound_path = sound_path
        self._lock = threading.Lock()
        self._ensure_sound_exists()

    def _ensure_sound_exists(self):
        if not os.path.exists(self.sound_path):
            self._generate_siren_wav()

    def _generate_siren_wav(self, duration=3.0):
        os.makedirs(os.path.dirname(self.sound_path), exist_ok=True)

        t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
        low_freq = 500
        high_freq = 950
        wiggle_rate = 1.5
        freq = low_freq + (high_freq - low_freq) * (0.5 + 0.5 * np.sin(2 * np.pi * wiggle_rate * t))
        phase = np.cumsum(2 * np.pi * freq / SAMPLE_RATE)
        waveform = np.sin(phase)

        envelope = np.minimum(t / 0.1, 1.0)
        envelope *= np.minimum((duration - t) / 0.15, 1.0)
        waveform = waveform * envelope

        amplitude = 0.5 * 32767
        samples = (waveform * amplitude).astype(np.int16)

        with wave.open(self.sound_path, "w") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(SAMPLE_RATE)
            wav_file.writeframes(samples.tobytes())

        print(f"[SIREN] Sound file created: {self.sound_path}")

    def play(self):
        if not os.path.exists(self.sound_path):
            self._ensure_sound_exists()
        with self._lock:
            try:
                self._play_platform()
            except Exception as e:
                print(f"[SIREN ERROR] Could not play sound: {e}")

    def _play_platform(self):
        system = platform.system()
        if system == "Windows":
            import winsound
            winsound.PlaySound(self.sound_path, winsound.SND_FILENAME)
        elif system == "Darwin":
            subprocess.Popen(["afplay", self.sound_path])
        else:
            for player in ("aplay", "paplay", "play"):
                try:
                    subprocess.Popen([player, self.sound_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    return
                except FileNotFoundError:
                    continue
            print("[SIREN] No audio player found (aplay/paplay/play).")

    def play_async(self):
        thread = threading.Thread(target=self.play, daemon=True)
        thread.start()

    def test(self):
        print("[SIREN] Testing siren sound...")
        self.play_async()


if __name__ == "__main__":
    SirenPlayer().test()