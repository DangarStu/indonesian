import os
import sys
from google.cloud import texttospeech

# ✅ Check command-line usage
if len(sys.argv) != 2:
    print("Usage: python tts_generate.py <ssml_file.xml>")
    sys.exit(1)

# 📥 Get input filename
xml_filename = sys.argv[1]

# 📤 Determine output filename
if not xml_filename.endswith(".xml"):
    print("❌ Error: Input file must be an .xml file")
    sys.exit(1)

mp3_filename = xml_filename.replace(".xml", ".mp3")

# 🔐 Set path to your Google Cloud service account key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service-account-key.json"

# 📄 Read SSML content
with open(xml_filename, "r", encoding="utf-8") as f:
    ssml_text = f.read()

# 🎤 Create TTS client
client = texttospeech.TextToSpeechClient()

synthesis_input = texttospeech.SynthesisInput(ssml=ssml_text)

# ⚙️ Required voice settings (still needed even with SSML <voice> tags)
voice = texttospeech.VoiceSelectionParams(
    language_code="id-ID", name="id-ID-Standard-A"
)

audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

# 🚀 Send request
response = client.synthesize_speech(
    input=synthesis_input,
    voice=voice,
    audio_config=audio_config
)

# 💾 Save MP3 output
with open(mp3_filename, "wb") as out:
    out.write(response.audio_content)

print(f"✅ MP3 file saved to {mp3_filename}")
