import requests
from bs4 import BeautifulSoup
from requests_toolbelt.multipart.encoder import MultipartEncoder
from pydantic import BaseModel, validator
from typing import Optional


class KPPanel(BaseModel):
    scientific_name: Optional[str]
    higher_classification: Optional[str]
    family: Optional[str]
    rank: Optional[str]
    kingdom: Optional[str]
    phylum: Optional[str]

    @validator('scientific_name')
    def remove_underscore(cls, v):
        if v:
            return v.replace("_", " ")
        return v


class SearchByImageResponse(BaseModel):
    search_bar: Optional[str]
    kb_panel: KPPanel = KPPanel()

    class Config:
        extra = "ignore"


def search_by_image(filename: str, content: bytes, content_type: str):
    """
    based on this manual http://slpython.blogspot.com/2015/03/google-kereses-kep-alapjan-python-alol.html
    """
    # * setup the multipart data form function input
    multipart_data = dict(
        encoded_image=(filename, content, content_type),
        image_url=None,
        image_content=None,
        filename=filename,
        btnG=None,
    )
    m = MultipartEncoder(multipart_data)

    # * setup user agent using https://github.com/jnrbsn/user-agents
    ua_url = "https://jnrbsn.github.io/user-agents/user-agents.json"
    ua = requests.get(ua_url).json()[0]

    # * setup the headers
    headers = {"Content-Type": m.content_type, "User-Agent": ua}

    # * google search by image
    r = requests.post(
        "https://www.google.com/searchbyimage/upload",
        params={"hl": "en-US"},
        data=m,
        headers=headers,
        allow_redirects=False,
    )

    # * redirect to the search results
    redirect_location = r.headers["Location"]

    # * get the search results
    r = requests.get(redirect_location, headers=headers, params={"hl": "en-US"})

    # * parse the search results
    soup = BeautifulSoup(r.text, "html.parser")

    # * init response model
    search_response = SearchByImageResponse()

    # * get text from input search bar
    bar = soup.find("input", {"aria-label": "Search"})
    if bar:
        # print("bar", bar.get("value"))
        search_response.search_bar = bar.get("value")

    # * get right kb panel
    kb_panel = soup.find_all("div", {"class": "kp-blk"})
    if kb_panel:
        panel = {}
        for divs in kb_panel[0].find_all("div", {"class": "zloOqf PZPZlf"}):
            # print(divs.get_text())
            k, v = divs.get_text().split(": ")
            k = k.replace("\n", "").replace(" ", "_").strip().lower()
            v = v.replace("\n", "").replace(" ", "_").strip().lower()
            panel[k] = v
        search_response.kb_panel = KPPanel(**panel)

    return search_response
