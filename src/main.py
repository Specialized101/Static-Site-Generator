import os, shutil

from utils import markdown_to_html_node, extract_title

def main():
    src = "static"
    dst = "public"
    src_path = "content/index.md"
    dest_path = "public/index.html"
    template_path = "template.html"
    if os.path.exists(os.path.abspath(dst)):
        shutil.rmtree(os.path.abspath(dst))
    os.makedirs(os.path.abspath(dst), exist_ok=True)

    copy_static(src, dst)

    generate_page(src_path, template_path, dest_path)

def copy_static(src, dst):
    src_path = os.path.abspath(src)
    dst_path = os.path.abspath(dst)
    files = os.listdir(src_path)
    for file in files:
        file_path = os.path.join(src_path, file)
        if os.path.isfile(file_path):
            print(f"Copying {file_path} to {os.path.join(dst_path, file)}")
            shutil.copy(file_path, os.path.join(dst_path, file))
        else:
            os.makedirs(os.path.join(dst_path, file), exist_ok=True)
            copy_static(file_path, os.path.join(dst_path, file))


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    src_abs_path = os.path.abspath(from_path)
    dest_abs_path = os.path.abspath(dest_path)
    template_abs_path = os.path.abspath(template_path)
    with open(src_abs_path) as f:
        content_text = f.read()
    with open(template_abs_path) as f:
        template_text = f.read()
    
    html = markdown_to_html_node(content_text).to_html()
    title = extract_title(content_text)
    template_text = template_text.replace("{{ Title }}", title)
    template_text = template_text.replace("{{ Content }}", html)

    os.makedirs(os.path.dirname(dest_abs_path), exist_ok=True)
    with open(dest_abs_path, "w") as f:
        f.write(template_text)

if __name__ == "__main__":
    main()