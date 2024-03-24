from pydub import AudioSegment
import os

def downsample_mp3(input_file, output_file, target_size_mb):
    audio = AudioSegment.from_mp3(input_file)
    target_bitrate_kb = (target_size_mb * 8192) / len(audio)  # Target size in KB/s
    audio.export(output_file, format="mp3", bitrate=f"{int(target_bitrate_kb)}k")

def downsample_directory(source_directory, target_directory, target_size_mb):
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    for filename in os.listdir(source_directory):
        if filename.endswith(".mp3"):
            input_file = os.path.join(source_directory, filename)
            output_file = os.path.join(target_directory, filename)
            downsample_mp3(input_file, output_file, target_size_mb)
            print(f"{input_file} downsampled and saved to {output_file}")


def run(source, target, sz):
    downsample_directory(source, target, sz)


if __name__ == "__main__":
    source_directory = "../data/audio"  
    target_directory = "../data/audio/downsampled/"  
    target_sz = 22.5
    run(source_directory, target_directory, target_sz)