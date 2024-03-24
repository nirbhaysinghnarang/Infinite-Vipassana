import os

def compose_files_in_directory(source_directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for root, dirs, files in os.walk(source_directory):
        for dir_name in dirs:
            input_dir = os.path.join(source_directory, dir_name)
            output_file = os.path.join(output_directory, f"{dir_name}.txt")

            with open(output_file, 'w') as outfile:
                for filename in sorted(os.listdir(input_dir)):
                    if filename.endswith(".txt"):
                        filepath = os.path.join(input_dir, filename)
                        with open(filepath, 'r') as infile:
                            outfile.write(infile.read() + "\n")

source_directory = "../data/txt/transcribed"  
output_directory = "../data/txt/composed" 

compose_files_in_directory(source_directory, output_directory)
