import os, shutil

def main():
    copy_static("static", "public")

def copy_static(src, dst):
    if os.path.exists(os.path.abspath(dst)):
        shutil.rmtree(os.path.abspath(dst))
    os.mkdir(os.path.abspath(dst))
    copy_static_r(src, dst)

def copy_static_r(src, dst):
    src_path = os.path.abspath(src)
    dst_path = os.path.abspath(dst)
    files = os.listdir(src_path)
    for file in files:
        file_path = os.path.join(src_path, file)
        if os.path.isfile(file_path):
            shutil.copy(file_path, os.path.join(dst_path, file))
        else:
            os.makedirs(os.path.join(dst_path, file), exist_ok=True)
            copy_static_r(file_path, os.path.join(dst_path, file))


if __name__ == "__main__":
    main()