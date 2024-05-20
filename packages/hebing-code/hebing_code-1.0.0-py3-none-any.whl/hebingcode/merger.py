import os

def merge_files(source_dir, base_output_filepath):
    exclude_dirs = ['.git', 'target']
    included_extensions = ('.java', '.h', '.cpp')
    max_chars = 2000

    current_chars = 0
    file_count = 1
    outfile = None

    def open_new_file():
        nonlocal outfile, file_count, current_chars
        if outfile:
            outfile.close()
        outfile = open(f"{base_output_filepath}_{file_count}.txt", 'w', encoding='utf-8')
        current_chars = 0

    try:
        outfile = open(f"{base_output_filepath}_{file_count}.txt", 'w', encoding='utf-8')
    except Exception as e:
        print(f"Error opening output file: {e}")
        return

    for root, dirs, files in os.walk(source_dir):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            if file.endswith(included_extensions):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        content = infile.read()
                        content_length = len(content) + len(file_path) + 2
                        if current_chars + content_length > max_chars:
                            open_new_file()
                        outfile.write("\n" + file_path + "\n")
                        outfile.write(content)
                        current_chars += content_length
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

    if outfile:
        outfile.close()

def main():
    import sys
    source_directory = sys.argv[1]
    output_filepath = sys.argv[2]
    merge_files(source_directory, output_filepath)

if __name__ == "__main__":
    main()

