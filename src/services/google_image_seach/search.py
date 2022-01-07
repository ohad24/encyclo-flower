import requests
from bs4 import BeautifulSoup
from requests_toolbelt.multipart.encoder import MultipartEncoder
from pprint import pprint
import base64




def search_by_image(encoded_image):
    # http://slpython.blogspot.com/2015/03/google-kereses-kep-alapjan-python-alol.html
    content = base64.b64decode(encoded_image)
    m = MultipartEncoder(
        {
            "encoded_image": ("filename", content, "image/jpeg"),
            "image_url": None,
            "image_content": None,
            "filename": None,
            "btnG": None,
        }
    )
    # * https://github.com/jnrbsn/user-agents
    ua_url = "https://jnrbsn.github.io/user-agents/user-agents.json"
    ua = requests.get(ua_url).json()[0]
    # print(ua)
    headers = {"Content-Type": m.content_type, "User-Agent": ua}
    r = requests.post(
        "https://www.google.com/searchbyimage/upload",
        params={"hl": "en-US"},
        data=m,
        headers=headers,
        allow_redirects=False,
    )
    location = r.headers["Location"]
    r = requests.get(location, headers=headers, params={"hl": "en-US"})
    # print(r.status_code)
    soup = BeautifulSoup(r.text, "html.parser")

    # * get text from input search bar
    bar = soup.find("input", {"aria-label": "Search"})
    if bar:
        print('bar', bar.get("value"))

    # * get right kb panel
    kb_panel = soup.find_all("div", {"class": "kp-blk"})
    if kb_panel:
        for divs in kb_panel[0].find_all("div", {"class": "zloOqf PZPZlf"}):
            print(divs.get_text())
    print("---")


if __name__ == "__main__":
    test_images = ["I3YOFNKFFRVZOPN.jpg", "IWU8AAVDDDEEKRC.jpg", "58NY77V207Q7H06.jpg"]
    images_directory = "tests/assets/images/"

    for file in test_images:
        with open(images_directory + file, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
            response = search_by_image(encoded_image)
            print(response)
