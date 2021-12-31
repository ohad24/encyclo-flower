## Download images from google

**the pypi package [google_images_download ](https://pypi.org/project/google_images_download/) is broken.**

### **Solution**:
From [StackOverflow](https://stackoverflow.com/questions/60370799/google-image-download-with-python-cannot-download-images?answertab=votes#tab-top)

Using **Joeclinton1/google-images-download** repository.

You need to create scientific_names.txt in the same directory as this script.

```bash
git clone https://github.com/Joeclinton1/google-images-download.git
cd google-images-download && sudo python setup.py install
```