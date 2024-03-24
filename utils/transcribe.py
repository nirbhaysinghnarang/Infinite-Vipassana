import os
from load_dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

def transcribe_audio_file(infile, outfile):
    audio_file = open(infile, "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
    )
    with open(outfile, 'w') as out_file:
        out_file.write(transcription.text)

def transcribe_nested_directories(source_directory, target_directory):
    for root, dirs, files in os.walk(source_directory):
        for filename in files:
            if filename.endswith(".mp3"):
                infile = os.path.join(root, filename)
                rel_path = os.path.relpath(infile, source_directory)
                out_dir = os.path.join(target_directory, os.path.dirname(rel_path))
                if not os.path.exists(out_dir):
                    os.makedirs(out_dir)
                outfile = os.path.join(out_dir, os.path.splitext(filename)[0] + ".txt")
                transcribe_audio_file(infile, outfile)

source_directory = "../data/audio/chunked"  
target_directory = "../data/txt/transcribed" 

transcribe_nested_directories(source_directory, target_directory)
