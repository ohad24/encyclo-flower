from google_images_download import google_images_download
import os

# scientific_names is a list of scientific names from the database
current_script_location = os.path.dirname(__file__)
scientific_names = open(
    os.path.join(current_script_location, "scientific_names.txt"), "r"
).readlines()

downloader = google_images_download.googleimagesdownload()

DOWNLOAD_LIMIT = 100

for scientific_name in scientific_names[:2]:
    # * arguments docs https://google-images-download.readthedocs.io/en/latest/arguments.html#
    arguments = {
        "keywords": '"' + scientific_name + '"',
        "limit": DOWNLOAD_LIMIT,
        "print_urls": True,
        "output_directory": os.path.dirname(__file__) + "/downloads/",
        "image_directory": scientific_name,
        "extract_metadata": True,
        "size": ">1024*768",
        "delay": 0.5,
    }
    paths = downloader.download(arguments)


# move metadata file to downloads folder for each scientific name
# scripts/download_google_images/google-images-download/logs/
def list_log_files():
    logs_files_name = os.listdir(
        os.path.dirname(__file__) + "/google-images-download/logs/"
    )
    return logs_files_name


# remove all files in log folder. remove ' and " from file name
for file_name in list_log_files():
    new_file_name = file_name.replace('"', "").replace("'", "")
    os.rename(
        os.path.dirname(__file__) + "/google-images-download/logs/" + file_name,
        os.path.dirname(__file__) + f"/downloads/{new_file_name[:-5]}/" + new_file_name,
    )
