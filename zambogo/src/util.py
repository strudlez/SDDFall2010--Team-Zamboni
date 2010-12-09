import os
import dirs

def get_data_dir():
    return dirs.datadir

def get_image_dir():
    return os.path.join(get_data_dir(), "images")

def get_image(name):
    return os.path.join(get_image_dir(), name)

def get_home_dir():
    return os.path.expanduser("~")

def __ensure_dir_exists(path):
    if os.path.exists(path):
        return
    else:
        os.makedirs(path)

def get_ggo_user_dir():
    dir = os.path.join(get_home_dir(), ".ggo")
    __ensure_dir_exists(dir)
    return dir

def get_sgf_dir():
    dir = os.path.join(get_ggo_user_dir(),"sgf")
    __ensure_dir_exists(dir)
    return dir
