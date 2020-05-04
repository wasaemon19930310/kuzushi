# -*- coding: SHIFT-JIS -*-
from flask import Flask, render_template, request
import numpy as np
import cv2
from werkzeug.utils import secure_filename
import io
import os
import h5py as h5
from dictionary import Dictionary

app = Flask(__name__, static_url_path='/static')

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def sendFile():
    result = []
    label = []
    link = []

    if request.method == 'POST':
        file = request.files['img_file']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path_name = "/static/tmp/" + filename
            dictionary = Dictionary(file)
            res = dictionary.judgePhoto()

            for i, acc in enumerate(res):
                if int(acc * 100) > 0:
                    val = int(acc * 100)
                    src = dictionary.getLabel(i)
                    dst = src.replace('U+', '\\u')

                    uc01 = dst.encode('utf-8')
                    uc02 = uc01.decode('utf-8')
                    uc03 = uc02.encode().decode('unicode-escape')

                    label.append(uc03)
                    result.append(val)
                    link.append(src)
            return render_template("result.html", result = result, label = label, link = link, image_path = save_path_name)
    else:
        path = '/var/www/html/static/tmp/'
        files = os.listdir(path)
        for i in range(len(files)):
            os.remove(path + files[i])
        return render_template("index.html")
        
@app.route('/.well-known/acme-challenge/<filename>')
def well_known(filename):
    return render_template('.well-known/acme-challenge/' + filename)

if __name__ == '__main__':
    app.run()
