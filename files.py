import os
from collections import defaultdict
import pyperclip

def find_files_recursively(root_dir, target_files):
    """
    Traverse the directory tree rooted at root_dir, looking for files with names in target_files.
    Return a dictionary with file types as keys and list of paths as values.
    """
    found_files = defaultdict(list)
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename in target_files:
                file_extension = os.path.splitext(filename)[1]
                found_files[file_extension].append(os.path.join(dirpath, filename))
    return found_files

def write_files_to_txt(file_dict, output_filename):
    """
    Write the contents of the found files to the output file.
    Group files by their type and include their size and content.
    """
    try:
        with open(output_filename, 'w') as output_file:
            for file_type, files in file_dict.items():
                output_file.write(f"== File Type: {file_type} ==\n\n")
                for file in files:
                    if os.path.isfile(file):
                        with open(file, 'r') as input_file:
                            content = input_file.read()
                        
                        file_size = os.path.getsize(file)
                        file_details = (
                            f"File: {file}\n"
                            f"Size: {file_size} bytes\n"
                            f"{'=' * 40}\n\n"
                        )
                        
                        output_file.write(file_details)
                        output_file.write(content)
                        output_file.write('\n\n')
                    else:
                        output_file.write(f"File: {file}\n")
                        output_file.write("Error: File not found.\n")
                        output_file.write(f"{'=' * 40}\n\n")
        
        print(f"Contents written to {output_filename}")
        
        # Copy output file path to clipboard
        pyperclip.copy(os.path.abspath(output_filename))
        print(f"The output file path has been copied to the clipboard: {os.path.abspath(output_filename)}")
        
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
if __name__ == "__main__":
    # List of files to be written to the output file
    target_files = ['index.html', 'styles.css', 'calculator.html', 'scripts.js', 'results.html']
    # Directory to start the search
    root_directory = '.'
    # Name of the output file
    output_file = 'combined_output.txt'
    
    # Find files recursively
    files_to_write = find_files_recursively(root_directory, target_files)
    
    # Write found files to the output file
    write_files_to_txt(files_to_write, output_file)