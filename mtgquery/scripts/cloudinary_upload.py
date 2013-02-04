import os
import cloudinary
from cloudinary import uploader
from mtgquery.lib.util import rel_path
from mtgquery.lib.cloudinary import config_cloudinary
from eventlet import GreenPool
pool = GreenPool(size=10)


def upload_image(root_folder, image_path, counter=None, print_result=False):
    loc = root_folder + "/" + image_path
    short_name = image_path.split(".")[0]
    short_name = short_name.replace("/", "_")
    uploader.upload(loc, public_id=short_name)
    if print_result:
        print "Uploaded {}".format(loc)


def upload_card_images(root_folder):
    for path in os.listdir(root_folder):
        pool.spawn_n(upload_image, root_folder, path, print_result=True)
    pool.waitall()
    print "Cards Complete!"


def upload_icons(root_folder):
    for size_folder in os.listdir(root_folder):
        for icon in os.listdir("{}/{}".format(root_folder, size_folder)):
            pool.spawn_n(upload_image, root_folder, "{}/{}".format(size_folder, icon), print_result=True)
    pool.waitall()
    print "Icons Complete!"

if __name__ == "__main__":
    REL = rel_path(__file__)
    config_cloudinary(cloudinary, REL + os.sep + "credentials_cloudinary")
    root = """D:/Workspace/PythonWorkspace/mtg_env/mtgquery/mtgquery/mtg_images"""
    card_images = root + "/card_images"
    icon_images = root + "/icons"
    upload_card_images(card_images)
    upload_icons(icon_images)
