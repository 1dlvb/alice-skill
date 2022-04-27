from PIL import Image
import requests

url = 'https://kinopoiskapiunofficial.tech/images/posters/kp/530.jpg'


def crop_img(url):
    resp = requests.get(url, stream=True).raw
    img = Image.open(resp)
    z = img.size
    r = z[1]/400
    print(img.size)
    new_url = img.resize((int(z[0]/r), int(z[1]/r)))
    print(new_url.size)
    return new_url

print(crop_img(url))
