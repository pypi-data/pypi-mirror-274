import os
import subprocess
import sys
import os

def process_image(input_image_path, output_directory):
    # Get the directory containing the run.py script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the path to the image_processor executable
    executable = os.path.join(script_dir, "image_processor")

    if not os.path.exists(executable):
        print(f"Error: The image_processor executable '{executable}' does not exist.")
        sys.exit(1)

    # Construct the command
    command = [executable, input_image_path, output_directory]

    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout.decode())
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr.decode()}")
        sys.exit(1)


def main():
    if len(sys.argv) != 3:
        print("Usage: python run.py input_image_path output_directory")
        sys.exit(1)
    
    input_image_path = sys.argv[1]
    output_directory = sys.argv[2]

    process_image(input_image_path, output_directory)

if __name__ == "__main__":
    main()

