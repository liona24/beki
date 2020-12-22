import sys
import os
import shutil
import glob
import subprocess

if __name__ == '__main__':
    dst_dir = "dist/"

    bundle_dir = os.path.join(dst_dir, "bundle")
    app_dir = os.path.join(bundle_dir, "app")
    tex_dir = os.path.join(bundle_dir, "tex")
    if os.path.exists(bundle_dir):
        shutil.rmtree(bundle_dir)

    os.makedirs(app_dir)
    os.makedirs(tex_dir)

    print("Collecting backend ..")
    for f in glob.glob("backend/*.py"):
        if "settings" in f:
            continue
        print(f)
        shutil.copy(f, app_dir)

    print("Collecting TeX files ..")
    for f in glob.glob("tex/*"):
        print(f)
        shutil.copy(f, tex_dir)

    print("Building frontend ..")
    rv = subprocess.call(["yarn", "build"], cwd="beki")
    if rv != 0:
        print("Failed.")
        exit(rv)

    print("Done.")
