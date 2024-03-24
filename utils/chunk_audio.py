from pydub import AudioSegment
import os

def split_mp3(input_file, output_directory):
    audio = AudioSegment.from_mp3(input_file)
    duration = len(audio)
    segment_duration = duration // 5

    for i in range(3):
        start_time = i * segment_duration
        end_time = (i + 1) * segment_duration
        segment = audio[start_time:end_time]
        output_file = os.path.join(output_directory, f"part_{i+1}.mp3")
        segment.export(output_file, format="mp3")
        print(f"Segment {i+1} saved to {output_file}")

def split_directory(source_directory, target_directory):
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    for filename in os.listdir(source_directory):
        if filename.endswith(".mp3"):
            input_file = os.path.join(source_directory, filename)
            output_dir = os.path.join(target_directory, os.path.splitext(filename)[0])
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            split_mp3(input_file, output_dir)

def run(source, target):
    split_directory(source, target)

if __name__ == "__main__":
    source_directory = "../data/audio/downsampled"  
    target_directory = "../data/audio/chunked/by_5"  
    run(source_directory, target_directory)
