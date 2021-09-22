from flask import Flask
application=Flask(__name__)
app=application
if __name__ == '__main__':
    application.run(debug=True)

@application.route('/')
def hello_world():
    return "hello World!!"

""""import os
from pathlib import WindowsPath
from flask import Flask, render_template, url_for, request
from PIL import Image, ImageEnhance
from flask.helpers import send_from_directory
from werkzeug.utils import secure_filename
import cv2  # for image processing
import numpy as np  # to store image
import sys
import matplotlib.pyplot as plt
import numpy as np
from PIL import ImageTk, Image
UPLOAD_FOLDER = '../image/upload'
UPDATED_FOLDER = '../image/updated'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
imgname = ""


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


application = Flask(__name__)
app=application
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPDATED_FOLDER'] = UPDATED_FOLDER


@app.route('/')
@app.route("/home")
def home():
    return render_template('index.html')


@app.route('/upload/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route('/updated/<name>')
def send(name):
    return send_from_directory(UPDATED_FOLDER, name)


@app.route('/r/<filename>', methods=['GET', 'POST'])
def r(filename):
    if request.method == 'POST':
        img = Image.open(
            '../image/upload/'+filename)
        print(img.size)
        height = int(request.form['height'])
        width = int(request.form['width'])
        newsize = (height, width)
        img_resized = img.resize(newsize)
        print(img_resized.size)
        img_resized.save("updated/"+filename)
        return render_template('preview.html', filename=filename)


@app.route("/fileup", methods=['GET', 'POST'])
def fileup():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template('edit.html', filename=filename)


@app.route("/blue/<filename>", methods=['GET', 'POST'])
def blue(filename):
    originalmage = cv2.imread(
        '../image/upload/'+filename)
    print(originalmage.shape)
    originalmage = cv2.cvtColor(originalmage, cv2.COLOR_BGR2RGB)
    if originalmage is None:
        print("Can not find any image. Choose appropriate file")
        sys.exit()
    ReSized1 = cv2.resize(originalmage, (960, 540))
    name = 'blue_image_'+filename
    os.chdir('../image/updated')
    cv2.imwrite(name, ReSized1)
    print(name)
    return render_template('preview.html', filename=name)


@app.route("/grey/<filename>", methods=['GET', 'POST'])
def grey(filename):
    originalmage = cv2.imread(
        '../image/upload/'+filename)
    print(originalmage.shape)
    if originalmage is None:
        print("Can not find any image. Choose appropriate file")
        sys.exit()
    grayScaleImage = cv2.cvtColor(originalmage, cv2.COLOR_BGR2GRAY)
    ReSized2 = cv2.resize(grayScaleImage, (960, 540))
    name = ('grey_image_'+filename)
    os.chdir('../image/updated')
    cv2.imwrite(name, ReSized2)
    return render_template('preview.html', filename=name)


@app.route("/color/<filename>", methods=['GET', 'POST'])
def color(filename):
    originalmage = cv2.imread(
        '../image/upload/'+filename)
    print(originalmage.shape)
    if originalmage is None:
        print("Can not find any image. Choose appropriate file")
        sys.exit()
    colorImage = cv2.bilateralFilter(originalmage, 15, 75, 75)
    ReSized5 = cv2.resize(colorImage, (960, 540))
    name = ('Polished_image_'+filename)
    os.chdir('../image/updated')
    cv2.imwrite(name, ReSized5)
    return render_template('preview.html', filename=name)


@app.route("/cartoon/<filename>", methods=['GET', 'POST'])
def cartoon(filename):
    originalmage = cv2.imread(
        '../image/upload/'+filename)
    print(originalmage.shape)
    if originalmage is None:
        print("Can not find any image. Choose appropriate file")
        sys.exit()
    grayScaleImage = cv2.cvtColor(originalmage, cv2.COLOR_BGR2GRAY)
    smoothGrayScale = cv2.medianBlur(grayScaleImage, 5)
    getEdge = cv2.adaptiveThreshold(grayScaleImage, 225,
                                    cv2.ADAPTIVE_THRESH_MEAN_C,
                                    cv2.THRESH_BINARY, 9, 9)
    colorImage = cv2.bilateralFilter(originalmage, 15, 75, 75)
    cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask=getEdge)
    ReSized6 = cv2.resize(cartoonImage, (960, 540))
    name = ('carrtoon_image_'+filename)
    os.chdir('../image/updated')
    cv2.imwrite(name, ReSized6)
    return render_template('preview.html', filename=name)


@app.route("/smooth/<filename>", methods=['GET', 'POST'])
def smooth(filename):
    originalmage = cv2.imread(
        '../image/upload/'+filename)
    print(originalmage.shape)
    if originalmage is None:
        print("Can not find any image. Choose appropriate file")
        sys.exit()
    smoothGrayScale = cv2.medianBlur(originalmage, 5)
    ReSized3 = cv2.resize(smoothGrayScale, (960, 540))
    name = ('smooth_image_'+filename)
    os.chdir('../image/updated')
    cv2.imwrite(name, ReSized3)
    return render_template('preview.html', filename=name)


@app.route("/edge/<filename>", methods=['GET', 'POST'])
def edge(filename):
    originalmage = cv2.imread(
        '../image/upload/'+filename)
    print(originalmage.shape)
    if originalmage is None:
        print("Can not find any image. Choose appropriate file")
        sys.exit()
    grayScaleImage = cv2.cvtColor(originalmage, cv2.COLOR_BGR2GRAY)
    smoothGrayScale = cv2.medianBlur(grayScaleImage, 5)
    getEdge = cv2.adaptiveThreshold(grayScaleImage, 225,
                                    cv2.ADAPTIVE_THRESH_MEAN_C,
                                    cv2.THRESH_BINARY, 9, 9)
    ReSized4 = cv2.resize(getEdge, (960, 540))
    name = ('Edge_image_'+filename)
    os.chdir('../image/updated')
    cv2.imwrite(name, ReSized4)
    return render_template('preview.html', filename=name)


@ app.route("/about")
def about():
    return render_template('about.html')


@ app.route("/editing/<filename>", methods=['POST', 'GET'])
def editing(filename):
    return render_template('resize.html', filename=filename)


@ app.route("/edit")
def edit():
    return render_template('edit.html')


@ app.route("/contact")
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)
    """
