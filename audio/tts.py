from google.cloud import texttospeech_v1 as texttospeech
import os
import re

# Set your service account key file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service-account-key.json"

# Load full SSML content
with open("indonesian_number_drill_100.xml", "r", encoding="utf-8") as f:
    full_ssml = f.read()

# Extract individual <p> blocks
paragraphs = re.findall(r"<p>.*?</p>", full_ssml, re.DOTALL)

# Break into chunks that stay under 5000 bytes when wrapped in <speak>...</speak>
chunks = []
current_chunk = ""
for p in paragraphs:
    test_chunk = current_chunk + p
    test_wrapped = f"<speak>{test_chunk}</speak>"
    if len(test_wrapped.encode("utf-8")) > 4900:
        chunks.append(current_chunk)
        current_chunk = p
    else:
        current_chunk = test_chunk
if current_chunk:
    chunks.append(current_chunk)

# Set up TTS client
client = texttospeech.TextToSpeechClient()

# Generate MP3 files for each chunk
for i, chunk in enumerate(chunks):
    print(f"🔊 Synthesizing part {i+1}/{len(chunks)}...")
    synthesis_input = texttospeech.SynthesisInput(ssml=f"<speak>{chunk}</speak>")

    voice = texttospeech.VoiceSelectionParams(
        language_code="id-ID",
        name="id-ID-Standard-A",  # Ignored because SSML defines voices
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    out_path = f"output_part_{i+1}.mp3"
    with open(out_path, "wb") as out:
        out.write(response.audio_content)
    print(f"✅ Saved: {out_path}")

