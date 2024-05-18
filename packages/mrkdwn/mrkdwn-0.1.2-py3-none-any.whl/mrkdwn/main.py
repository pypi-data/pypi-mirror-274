import argparse
import os
import sys
from pathlib import Path

def list_files(base_path, recurse, name_filters=None, filetype=None, condition=None):
    ignored_dirs = {'.git', '__pycache__'}
    file_dict = {}

    if recurse:
        walker = os.walk(base_path)
    else:
        walker = [(base_path, next(os.walk(base_path))[1], next(os.walk(base_path))[2])]

    for root, dirs, files in walker:
        dirs[:] = [d for d in dirs if d not in ignored_dirs]
        print(f"Processing directory: {root}")

        depth = root[len(base_path):].count(os.sep)

        relevant_files = [
            f for f in files if (
                (name_filters is None or any(f.startswith(n) for n in name_filters.split(' | '))) and
                (filetype is None or f.endswith(filetype)) and
                (condition is None or eval(condition, {"__builtins__": {}}, {"f": f}))
            )
        ]

        if relevant_files:
            header = '#' * (depth + 2)  # Parent directory is #, first level is ##
            file_dict[root] = {
                "header": header,
                "files": relevant_files
            }
            print(f"Adding {len(relevant_files)} files under: {root}")

    return file_dict

def read_file_with_fallback(file_path):
    encodings = ['utf-8', 'latin-1', 'iso-8859-1']
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                return file.read()
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError(f"Unable to decode {file_path} with any known encodings")

def write_markdown(file_dict, output_file, base_path):
    base_dir_name = os.path.basename(base_path.rstrip('/'))
    with open(output_file, 'w', encoding='utf-8') as md_file:
        print(f"Writing to {output_file}")
        for path, data in sorted(file_dict.items(), key=lambda x: x[0]):
            relative_path = os.path.relpath(path, base_path)
            if relative_path == '.':
                relative_path = base_dir_name
            md_file.write(f"{data['header']} {relative_path}\n")
            for filename in data['files']:
                file_ext = Path(filename).suffix.lstrip('.')
                if not file_ext:
                    file_ext = 'text'
                md_file.write(f"{data['header']}# {filename}\n")
                file_path = os.path.join(path, filename)
                try:
                    content = read_file_with_fallback(file_path)
                    md_file.write(f"```{file_ext}\n{content}\n```\n")
                except UnicodeDecodeError as e:
                    print(f"Error reading {file_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Generate a Markdown file from directory contents.")
    parser.add_argument("path", help="Path to the directory")
    parser.add_argument("-r", "--recurse", action='store_true', help="Recurse into subdirectories")
    parser.add_argument("-n", "--name", help="Filter files by name, separated by ' | '", type=str)
    parser.add_argument("-t", "--type", help="Filter files by file type")
    parser.add_argument("-o", "--output", help="Output markdown file name")
    parser.add_argument("-c", "--condition", help="Python code condition to filter files. Can be code or a file path starting with '@'", type=str)

    args = parser.parse_args()

    condition = None
    if args.condition:
        if args.condition.startswith('@'):
            condition_file = args.condition[1:]
            with open(condition_file, 'r') as f:
                condition = f.read().strip()
        else:
            condition = args.condition

    file_dict = list_files(args.path, args.recurse, name_filters=args.name, filetype=args.type, condition=condition)
    output_filename = args.output if args.output else f"{os.path.basename(args.path)}-{'-'.join(args.name.split(' | ') if args.name else ['marked']).replace(' ', '-')}.md"

    write_markdown(file_dict, output_filename, args.path)

if __name__ == "__main__":
    main()
