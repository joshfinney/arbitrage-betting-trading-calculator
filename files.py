import os
from collections import defaultdict
import pyperclip

def find_files_recursively(root_dir, target_files, ignored_dirs):
    """
    Traverse the directory tree rooted at root_dir, looking for files with names in target_files.
    Return a dictionary with file types as keys and list of paths as values.
    """
    found_files = defaultdict(list)
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Skip ignored directories
        dirnames[:] = [d for d in dirnames if d not in ignored_dirs]
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
        pyperclip.copy(os.path.abspath(output_filename))
        print(f"The output file path has been copied to the clipboard: {os.path.abspath(output_filename)}")
    except Exception as e:
        print(f"An error occurred: {e}")

def write_directory_tree(root_dir, output_filename, ignored_dirs):
    """
    Write the directory tree structure to the output file.
    """
    try:
        with open(output_filename, 'w') as output_file:
            for dirpath, dirnames, filenames in os.walk(root_dir):
                # Skip ignored directories
                dirnames[:] = [d for d in dirnames if d not in ignored_dirs]
                level = dirpath.replace(root_dir, '').count(os.sep)
                indent = ' ' * 4 * level
                output_file.write(f"{indent}{os.path.basename(dirpath)}/\n")
                subindent = ' ' * 4 * (level + 1)
                for filename in filenames:
                    output_file.write(f"{subindent}{filename}\n")
        print(f"Directory tree written to {output_filename}")
        pyperclip.copy(os.path.abspath(output_filename))
        print(f"The output file path has been copied to the clipboard: {os.path.abspath(output_filename)}")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    print("Choose a feature to run:")
    print("1. Find specific files and write to output file")
    print("2. Write directory tree to output file")
    choice = input("Enter the number of the feature you want to run: ")

    target_files = ['results.html', 'styles.css', 'scripts.js']
    root_directory = '.'
    ignored_dirs = ['.git', '__pycache__']

    if choice == '1':
        output_file = 'combined_output.txt'
        files_to_write = find_files_recursively(root_directory, target_files, ignored_dirs)
        write_files_to_txt(files_to_write, output_file)
    elif choice == '2':
        output_file = 'directory_tree.txt'
        write_directory_tree(root_directory, output_file, ignored_dirs)
    else:
        print("Invalid choice. Please run the program again and select a valid option.")

if __name__ == "__main__":
    main()