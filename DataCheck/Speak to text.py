from gtts import gTTS
import os

# Text to be converted to speech
text = "Hello, how are you today?"

# Language in which you want to convert
language = "en"

# Passing the text and language to the engine, slow=False to speak at normal speed
tts = gTTS(text=text, lang=language, slow=False)

# Saving the converted audio in a file named sample.mp3
tts.save("sample.mp3")

# Playing the converted file
os.system("start sample.mp3")