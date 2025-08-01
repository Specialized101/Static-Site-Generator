import os, shutil, sys

from utils import markdown_to_html_node, extract_title


def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    
    src = "static"
    dst = "docs"
    content_path = "content"
    template_path = "template.html"
    if os.path.exists(os.path.abspath(dst)):
        shutil.rmtree(os.path.abspath(dst))
    os.makedirs(os.path.abspath(dst), exist_ok=True)

    copy_static(src, dst)

    generate_pages_recursive(basepath, content_path, template_path, dst)

def copy_static(src, dst):
    src_path = os.path.abspath(src)
    dst_path = os.path.abspath(dst)
    files = os.listdir(src_path)
    for file in files:
        file_path = os.path.join(src_path, file)
        if os.path.isfile(file_path):
            print(f"Copying {src}/{file} → {dst}/{file}")
            shutil.copy(file_path, os.path.join(dst_path, file))
        else:
            os.makedirs(os.path.join(dst_path, file), exist_ok=True)    
            copy_static(os.path.join(src, file), os.path.join(dst, file))


def generate_page(basepath, from_path, template_path, dest_path):
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
    template_text = template_text.replace('href="/', f'href="{basepath}')
    template_text = template_text.replace('src="/', f'src="{basepath}')

    os.makedirs(os.path.dirname(dest_abs_path), exist_ok=True)
    with open(dest_abs_path, "w") as f:
        f.write(template_text)

def generate_pages_recursive(basepath, dir_path_content, template_path, dest_dir_path):
    content_abs = os.path.abspath(dir_path_content)
    files = os.listdir(content_abs)
    for file in files:
        file_abs = os.path.join(content_abs, file)
        if os.path.isfile(file_abs):
            if file.endswith(".md"):
                from_rel = os.path.join(dir_path_content, file)
                dest_rel = os.path.join(dest_dir_path, file.replace(".md", ".html"))
                generate_page(basepath, from_rel, template_path, dest_rel)
        else:
            os.makedirs(dest_dir_path, exist_ok=True)
            generate_pages_recursive(basepath, os.path.join(dir_path_content, file), template_path, os.path.join(dest_dir_path, file))

if __name__ == "__main__":
    main()