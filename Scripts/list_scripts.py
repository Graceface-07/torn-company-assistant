import os

def list_files(base_dir):
    for root, dirs, files in os.walk(base_dir):
        level = root.replace(base_dir, '').count(os.sep)
        indent = '    ' * level
        print(f"{indent}📁 {os.path.basename(root)}/")
        sub_indent = '    ' * (level + 1)
        for f in sorted(files):
            print(f"{sub_indent}📄 {f}")

# Replace 'scripts' with the full path if needed
if __name__ == "__main__":
    list_files("scripts")
