from statistics import mode
from io import BytesIO
import urllib

from flask import Flask
from flask import request
from PIL import Image

app = Flask(__name__)

KEY_COLOURS = {
    'teal': (0, 98, 110),
    'black': (36, 36, 36),
    'grey': (56, 70, 87),
    'navy': (0, 0, 80),
}
TOLERANCE = 100


@app.route('/api/image-tone', methods=['GET'])
def image_tone():
    url = request.args.get('url', None)
    if not url:
        return {'error': 'Missing URL'}, 400
    try:
        handle = urllib.request.urlopen(url)
    except Exception as e:
        return {'error': '%s' % e}, 500

    obj = BytesIO(handle.read())
    img = Image.open(obj)
    lft, upp, rght, low = img.getbbox()
    im = img.crop((lft, upp, rght / 2, low / 2))
    data = im.getdata()
    most_frequent = mode(data)
    # print('!!!%s' % repr(most_frequent))
    for key, values in KEY_COLOURS.items():
        s = 0
        for i, v in enumerate(values):
            s += (most_frequent[i] - v) ** 2
        diff = int(s / len(values))
        if diff < TOLERANCE:
            out = {"key": key}
            # out.update({'diff': diff})
            return out
    return {'key': None}, 404
