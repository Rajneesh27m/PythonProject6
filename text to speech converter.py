import tkinter as tk
from tkinter import ttk, scrolledtext, END
import pyttsx3


class TextToSpeechApp:
    def __init__(self, master):
        self.master = master
        master.title("Text-to-Speech Converter")

        # Text Input Area
        self.text_area = scrolledtext.ScrolledText(master, wrap=tk.WORD, height=15)
        self.text_area.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Voice Selection
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        self.voice_options = [voice.name for voice in voices]
        self.selected_voice = tk.StringVar(master)
        self.selected_voice.set(self.voice_options[0])  # Default to the first voice

        voice_label = tk.Label(master, text="Select Voice:")
        voice_label.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")
        voice_dropdown = ttk.Combobox(master, textvariable=self.selected_voice, values=self.voice_options)
        voice_dropdown.grid(row=1, column=1, padx=10, pady=(10, 0), sticky="ew")

        # Rate Control
        rate_label = tk.Label(master, text="Speech Rate:")
        rate_label.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="w")
        self.rate_scale = tk.Scale(master, from_=50, to=300, orient=tk.HORIZONTAL, command=self.update_rate)
        self.rate_scale.set(150)  # Default rate
        self.rate_scale.grid(row=2, column=1, padx=10, pady=(10, 0), sticky="ew")

        # Volume Control
        volume_label = tk.Label(master, text="Volume:")
        volume_label.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="w")
        self.volume_scale = tk.Scale(master, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL,
                                     command=self.update_volume)
        self.volume_scale.set(1)  # Default volume (max)
        self.volume_scale.grid(row=3, column=1, padx=10, pady=(10, 0), sticky="ew")

        # Buttons
        speak_button = tk.Button(master, text="Speak", command=self.speak_text)
        speak_button.grid(row=4, column=0, padx=10, pady=20, sticky="ew")

        stop_button = tk.Button(master, text="Stop", command=self.stop_speech)
        stop_button.grid(row=4, column=1, padx=10, pady=20, sticky="ew")

        clear_button = tk.Button(master, text="Clear", command=self.clear_text)
        clear_button.grid(row=4, column=2, padx=10, pady=20, sticky="ew")

        # Configure grid weights for resizing
        master.columnconfigure(0, weight=1)
        master.columnconfigure(1, weight=1)
        master.columnconfigure(2, weight=1)
        master.rowconfigure(0, weight=1)

    def update_rate(self, val):
        rate = int(float(val))
        self.engine.setProperty('rate', rate)

    def update_volume(self, val):
        volume = float(val)
        self.engine.setProperty('volume', volume)

    def speak_text(self):
        text = self.text_area.get("1.0", END)
        voice_id = [v.id for v in self.engine.getProperty('voices') if v.name == self.selected_voice.get()][0]
        self.engine.setProperty('voice', voice_id)

        self.engine.say(text)
        self.engine.runAndWait()

    def stop_speech(self):
        self.engine.stop()

    def clear_text(self):
        self.text_area.delete("1.0", END)


root = tk.Tk()
app = TextToSpeechApp(root)
root.mainloop()

