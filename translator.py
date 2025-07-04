import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
try:
    import pyperclip
except ImportError:
    pyperclip = None
try:
    import pyttsx3
except ImportError:
    pyttsx3 = None
import threading
try:
    from deep_translator import GoogleTranslator
    # Correct: instantiate before calling get_supported_languages
    _deep_translator_instance = GoogleTranslator(source='auto', target='en')
    DEEP_LANGUAGES = _deep_translator_instance.get_supported_languages(as_dict=True)
    del _deep_translator_instance
except ImportError:
    GoogleTranslator = None
    DEEP_LANGUAGES = {}

class LanguageTranslator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Language Translation Tool")
        self.root.geometry("800x600")
        # Modern light blue theme
        self.bg_main = '#e3f0fc'
        self.bg_frame = '#f7fbff'
        self.bg_entry = '#ffffff'
        self.bg_button = '#1976d2'
        self.fg_button = '#ffffff'
        self.fg_label = '#0d47a1'
        self.root.configure(bg=self.bg_main)
        # Use deep-translator if available
        if GoogleTranslator and DEEP_LANGUAGES:
            self.translator = GoogleTranslator
        else:
            self.translator = None
        if pyttsx3:
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', 150)
        else:
            self.tts_engine = None
        if self.translator:
            self.languages = DEEP_LANGUAGES
        else:
            # Fallback: Hardcoded language dictionary
            fallback_languages = {
                'en': 'english', 'fr': 'french', 'de': 'german', 'es': 'spanish', 'it': 'italian',
                'pt': 'portuguese', 'ru': 'russian', 'zh-cn': 'chinese (simplified)', 'ja': 'japanese',
                'ko': 'korean', 'ar': 'arabic', 'hi': 'hindi', 'bn': 'bengali', 'tr': 'turkish',
                'ta': 'tamil', 'te': 'telugu', 'ml': 'malayalam', 'ur': 'urdu', 'gu': 'gujarati',
                'mr': 'marathi', 'pa': 'punjabi', 'kn': 'kannada', 'fa': 'persian', 'pl': 'polish',
                'uk': 'ukrainian', 'vi': 'vietnamese', 'th': 'thai', 'id': 'indonesian', 'ms': 'malay',
                'sw': 'swahili', 'af': 'afrikaans', 'nl': 'dutch', 'sv': 'swedish', 'no': 'norwegian',
                'fi': 'finnish', 'da': 'danish', 'el': 'greek', 'he': 'hebrew', 'ro': 'romanian',
                'hu': 'hungarian', 'cs': 'czech', 'sk': 'slovak', 'hr': 'croatian', 'sr': 'serbian',
                'bg': 'bulgarian', 'et': 'estonian', 'lt': 'lithuanian', 'lv': 'latvian', 'sl': 'slovenian',
                'sq': 'albanian', 'ca': 'catalan', 'eo': 'esperanto', 'ga': 'irish', 'is': 'icelandic',
                'mt': 'maltese', 'cy': 'welsh', 'zu': 'zulu', 'xh': 'xhosa', 'yo': 'yoruba', 'ig': 'igbo',
                'am': 'amharic', 'so': 'somali', 'ne': 'nepali', 'si': 'sinhala', 'km': 'khmer', 'lo': 'lao',
                'my': 'myanmar (burmese)', 'jw': 'javanese', 'su': 'sundanese', 'fil': 'filipino', 'tl': 'tagalog',
                'mn': 'mongolian', 'kk': 'kazakh', 'uz': 'uzbek', 'ky': 'kyrgyz', 'tk': 'turkmen', 'ps': 'pashto',
                'ku': 'kurdish', 'az': 'azerbaijani', 'hy': 'armenian', 'ka': 'georgian', 'be': 'belarusian',
                'bs': 'bosnian', 'mk': 'macedonian', 'ceb': 'cebuano', 'haw': 'hawaiian', 'la': 'latin',
                'mi': 'maori', 'sm': 'samoan', 'gd': 'scots gaelic', 'yi': 'yiddish', 'yo': 'yoruba',
                'zu': 'zulu'
            }
            messagebox.showwarning("Warning", "No translation engine available. Using fallback language list.\nTranslation will be disabled.")
            self.languages = fallback_languages
        self.language_list = [(code, name.title()) for code, name in self.languages.items()]
        self.language_list.sort(key=lambda x: x[1])
        self.source_lang = tk.StringVar(value='auto')
        self.target_lang = tk.StringVar(value='en')
        self.setup_ui()

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background=self.bg_main)
        style.configure('TLabelframe', background=self.bg_frame)
        style.configure('TLabelframe.Label', background=self.bg_frame, foreground=self.fg_label, font=('Arial', 11, 'bold'))
        style.configure('TLabel', background=self.bg_frame, foreground=self.fg_label, font=('Arial', 11))
        style.configure('TButton', background=self.bg_button, foreground=self.fg_button, font=('Arial', 11, 'bold'))
        style.map('TButton', background=[('active', '#1565c0')])

        main_frame = ttk.Frame(self.root, padding="20", style='TFrame')
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        title_label = ttk.Label(main_frame, text="Language Translation Tool", font=('Arial', 18, 'bold'), background=self.bg_main, foreground=self.fg_label)
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        lang_frame = ttk.LabelFrame(main_frame, text="Language Selection", padding="10", style='TLabelframe')
        lang_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        lang_frame.columnconfigure(1, weight=1)
        lang_frame.columnconfigure(3, weight=1)
        ttk.Label(lang_frame, text="From:", style='TLabel').grid(row=0, column=0, padx=(0, 10))
        self.source_combo = ttk.Combobox(lang_frame, textvariable=self.source_lang, width=20, state="readonly")
        self.source_combo.grid(row=0, column=1, padx=(0, 20), sticky=(tk.W, tk.E))
        swap_btn = ttk.Button(lang_frame, text="⇄", width=3, command=self.swap_languages, style='TButton')
        swap_btn.grid(row=0, column=2, padx=5)
        ttk.Label(lang_frame, text="To:", style='TLabel').grid(row=0, column=3, padx=(20, 10))
        self.target_combo = ttk.Combobox(lang_frame, textvariable=self.target_lang, width=20, state="readonly")
        self.target_combo.grid(row=0, column=4, sticky=(tk.W, tk.E))
        self.populate_language_combos()

        input_frame = ttk.LabelFrame(main_frame, text="Input Text", padding="10", style='TLabelframe')
        input_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        input_frame.columnconfigure(0, weight=1)
        input_frame.rowconfigure(0, weight=1)
        self.input_text = scrolledtext.ScrolledText(input_frame, height=8, width=70, font=('Arial', 11), wrap=tk.WORD, bg=self.bg_entry)
        self.input_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        input_btn_frame = ttk.Frame(input_frame, style='TFrame')
        input_btn_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        clear_input_btn = ttk.Button(input_btn_frame, text="Clear", command=self.clear_input, style='TButton')
        clear_input_btn.pack(side=tk.LEFT, padx=(0, 10))
        paste_btn = ttk.Button(input_btn_frame, text="Paste", command=self.paste_text, style='TButton')
        paste_btn.pack(side=tk.LEFT, padx=(0, 10))
        self.translate_btn = ttk.Button(input_btn_frame, text="Translate", command=self.translate_text, style='TButton')
        self.translate_btn.pack(side=tk.RIGHT)

        output_frame = ttk.LabelFrame(main_frame, text="Translation", padding="10", style='TLabelframe')
        output_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        self.output_text = scrolledtext.ScrolledText(output_frame, height=8, width=70, font=('Arial', 11), wrap=tk.WORD, state='disabled', bg=self.bg_entry)
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        output_btn_frame = ttk.Frame(output_frame, style='TFrame')
        output_btn_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        copy_btn = ttk.Button(output_btn_frame, text="Copy", command=self.copy_translation, style='TButton')
        copy_btn.pack(side=tk.LEFT, padx=(0, 10))
        self.tts_btn = ttk.Button(output_btn_frame, text="🔊 Speak", command=self.speak_translation, style='TButton')
        self.tts_btn.pack(side=tk.LEFT, padx=(0, 10))
        clear_output_btn = ttk.Button(output_btn_frame, text="Clear", command=self.clear_output, style='TButton')
        clear_output_btn.pack(side=tk.LEFT)

        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W, background=self.bg_main, foreground=self.fg_label, font=('Arial', 10))
        status_bar.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        main_frame.rowconfigure(2, weight=1)
        main_frame.rowconfigure(3, weight=1)
        self.input_text.bind('<KeyRelease>', self.on_text_change)

    def populate_language_combos(self):
        source_values = ['auto - Detect Language'] + [f"{code} - {name}" for code, name in self.language_list]
        self.source_combo['values'] = source_values
        self.source_combo.set('auto - Detect Language')
        target_values = [f"{code} - {name}" for code, name in self.language_list]
        self.target_combo['values'] = target_values
        self.target_combo.set('en - English')

    def get_language_code(self, combo_value: str) -> str:
        return combo_value.split(' - ')[0]

    def swap_languages(self):
        if self.source_lang.get() != 'auto':
            current_source = self.source_combo.get()
            current_target = self.target_combo.get()
            source_code = self.get_language_code(current_source)
            target_code = self.get_language_code(current_target)
            self.target_combo.set(f"{source_code} - {self.languages[source_code].title()}")
            self.source_combo.set(f"{target_code} - {self.languages[target_code].title()}")
            input_text = self.input_text.get(1.0, tk.END).strip()
            output_text = self.output_text.get(1.0, tk.END).strip()
            if input_text and output_text and output_text != "Translation will appear here...":
                self.input_text.delete(1.0, tk.END)
                self.input_text.insert(1.0, output_text)
                self.clear_output()

    def on_text_change(self, event=None):
        text = self.input_text.get(1.0, tk.END).strip()
        if text:
            self.status_var.set("Ready to translate")
        else:
            self.status_var.set("Ready")

    def clear_input(self):
        self.input_text.delete(1.0, tk.END)
        self.status_var.set("Ready")

    def clear_output(self):
        self.output_text.config(state='normal')
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state='disabled')

    def paste_text(self):
        if pyperclip:
            try:
                clipboard_text = pyperclip.paste()
                if clipboard_text:
                    self.input_text.delete(1.0, tk.END)
                    self.input_text.insert(1.0, clipboard_text)
                    self.status_var.set("Text pasted")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to paste text: {str(e)}")
        else:
            messagebox.showerror("Error", "pyperclip is not installed.")

    def copy_translation(self):
        translation = self.output_text.get(1.0, tk.END).strip()
        if translation and translation != "Translation will appear here...":
            if pyperclip:
                try:
                    pyperclip.copy(translation)
                    self.status_var.set("Translation copied to clipboard")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to copy text: {str(e)}")
            else:
                messagebox.showerror("Error", "pyperclip is not installed.")
        else:
            messagebox.showwarning("Warning", "No translation to copy")

    def speak_translation(self):
        translation = self.output_text.get(1.0, tk.END).strip()
        if translation and translation != "Translation will appear here...":
            if self.tts_engine:
                def speak():
                    try:
                        self.tts_engine.say(translation)
                        self.tts_engine.runAndWait()
                    except Exception as e:
                        self.root.after(0, lambda: messagebox.showerror("Error", f"Text-to-speech failed: {str(e)}"))
                threading.Thread(target=speak, daemon=True).start()
                self.status_var.set("Speaking translation...")
            else:
                messagebox.showerror("Error", "pyttsx3 is not installed.")
        else:
            messagebox.showwarning("Warning", "No translation to speak")

    def translate_text(self):
        if not self.translator:
            messagebox.showerror("Translation Error", "Translation is not available because no translation engine is installed or working.\nYou can still use the language selection and other features.")
            return
        text = self.input_text.get(1.0, tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter text to translate")
            return
        source_code = self.get_language_code(self.source_combo.get())
        target_code = self.get_language_code(self.target_combo.get())
        if source_code == target_code and source_code != 'auto':
            messagebox.showwarning("Warning", "Source and target languages cannot be the same")
            return
        self.translate_btn.config(state='disabled')
        self.status_var.set("Translating...")
        def translate_worker():
            try:
                # Use deep-translator for translation
                detected_lang = source_code if source_code != 'auto' else 'auto'
                translated = self.translator(source=detected_lang, target=target_code).translate(text)
                detected_name = self.languages.get(detected_lang, detected_lang).title()
                self.root.after(0, lambda: self.update_translation_result(translated, detected_name, detected_lang))
            except Exception as e:
                self.root.after(0, lambda: self.handle_translation_error(str(e)))
        threading.Thread(target=translate_worker, daemon=True).start()

    def update_translation_result(self, translation: str, detected_lang_name: str, detected_lang_code: str):
        # Open a new window for the translation result
        result_window = tk.Toplevel(self.root)
        result_window.title("Translation Result")
        result_window.geometry("600x300")
        result_window.configure(bg='#f8f8ff')

        # Label for detected language
        if self.get_language_code(self.source_combo.get()) == 'auto':
            status = f"Translated from {detected_lang_name}"
        else:
            status = "Translation completed"
        status_label = ttk.Label(result_window, text=status, font=('Arial', 11, 'italic'))
        status_label.pack(pady=(10, 5))

        # Output text area (read-only)
        output_text = scrolledtext.ScrolledText(result_window, height=8, width=60, font=('Arial', 12), wrap=tk.WORD, state='normal')
        output_text.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        output_text.insert(1.0, translation)
        output_text.config(state='disabled')

        # Button frame
        btn_frame = ttk.Frame(result_window)
        btn_frame.pack(pady=(0, 10))

        # Copy button
        def copy_translation():
            if pyperclip:
                try:
                    pyperclip.copy(translation)
                    messagebox.showinfo("Copied", "Translation copied to clipboard", parent=result_window)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to copy text: {str(e)}", parent=result_window)
            else:
                messagebox.showerror("Error", "pyperclip is not installed.", parent=result_window)

        copy_btn = ttk.Button(btn_frame, text="Copy", command=copy_translation)
        copy_btn.pack(side=tk.LEFT, padx=(0, 10))

        # Speak button
        def speak_translation():
            if self.tts_engine:
                def speak():
                    try:
                        self.tts_engine.say(translation)
                        self.tts_engine.runAndWait()
                    except Exception as e:
                        self.root.after(0, lambda: messagebox.showerror("Error", f"Text-to-speech failed: {str(e)}", parent=result_window))
                threading.Thread(target=speak, daemon=True).start()
            else:
                messagebox.showerror("Error", "pyttsx3 is not installed.", parent=result_window)

        speak_btn = ttk.Button(btn_frame, text="🔊 Speak", command=speak_translation)
        speak_btn.pack(side=tk.LEFT, padx=(0, 10))

        # Close button
        close_btn = ttk.Button(btn_frame, text="Close", command=result_window.destroy)
        close_btn.pack(side=tk.LEFT, padx=(0, 10))

        # Update status and re-enable translate button in main window
        self.status_var.set(status)
        self.translate_btn.config(state='normal')

    def handle_translation_error(self, error_msg: str):
        self.status_var.set("Translation failed")
        self.translate_btn.config(state='normal')
        messagebox.showerror("Translation Error", f"Failed to translate text:\n{error_msg}\n\nPlease check your internet connection and try again.")

    def run(self):
        self.root.mainloop()

def main():
    try:
        app = LanguageTranslator()
        app.run()
    except Exception as e:
        # print(f"Error starting application: {e}")
        messagebox.showerror("Error", f"Failed to start application: {e}")

if __name__ == "__main__":
    main()
