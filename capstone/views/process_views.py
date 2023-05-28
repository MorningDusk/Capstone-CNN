from datetime import datetime
import io

from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.utils import redirect
import requests
import pytz
import base64

from capstone import db
from capstone.forms import ImageForm
from capstone.models import User
from capstone.models import Image

bp = Blueprint('process', __name__, url_prefix='/process')

def is_image_url(url):
    ext = url.split('.')[-1].lower()

    headers = requests.head(url).headers
    content_type = headers.get('Content-Type').lower() if 'Content-Type' in headers else ''

    if 'image' in content_type or ext in ['jpg', 'jpeg', 'png', 'gif']:
        return True
    else:
        return False

def request_process(id):
    data = {'value': id}
    url = 'http://112a-35-227-28-199.ngrok-free.app/process'
    response = requests.post(url, json=data)

    print(response.json()['result'])

    if response.status_code == 200:
        return response.json()['result']
    else:
        return None


@bp.route('/img', methods=('GET', 'POST'))
def img():
    form = ImageForm()
    if request.method == 'POST':
        if request.form['type'] == '저장':
            file = request.files['image-file']
            typ = int(request.form['PCB_type'])
            url = request.form['image-url']

            if file:
                user_id = session.get('user_id')
                time_now = datetime.now(pytz.timezone('Asia/Seoul'))
                image = Image(user=user_id, image=file.read(), type=typ, date=time_now)
                db.session.add(image)
                db.session.commit()

                flash("파일이 업로드되었습니다.")
                return render_template('process/img.html', form=form)
            elif len(url) != 0:
                if is_image_url(url):
                    response = requests.get(url)
                    if response.status_code == 200:
                        user_id = session.get('user_id')
                        time_now = datetime.now(pytz.timezone('Asia/Seoul'))
                        image = Image(user=user_id, image=response.content, type=typ, date=time_now)
                        db.session.add(image)
                        db.session.commit()

                        flash("파일이 업로드되었습니다.")
                        return render_template('process/img.html', form=form)
                    else:
                        flash("오류가 발생했습니다.")
                else:
                    flash("올바른 url을 입력해주세요.")
            else:
                flash("파일을 업로드해주세요.")

    return render_template('process/img.html', form=form)

@bp.route('/cam', methods=('GET', 'POST'))
def cam():
    if request.method == 'POST':
        if request.form.get('source') == 'javascript':
            user_id = session.get('user_id')
            typ = int(request.form.get('type'))
            time_now = datetime.now(pytz.timezone('Asia/Seoul'))
            data_url = request.form['image']
            data = base64.b64decode(data_url.split(',')[1])
            image = Image(user=user_id, image=data, type=typ, date=time_now)
            db.session.add(image)
            db.session.commit()

    return render_template('process/cam.html')

@bp.route('/result/<id>', methods=('GET', 'POST'))
def result(id):
    #id = request_process(id) # 머신러닝 서버

    image = Image.query.filter_by(id=id).first()
    image.image = base64.b64encode(image.image).decode('utf-8')
    if id != -1:
        return render_template('process/result.html', image=image)
    else:
        flash("이미지 분석에 실패했습니다.")

@bp.route('/captured', methods=('GET', 'POST'))
def captured():
    user_id = session.get('user_id')
    images = Image.query.filter_by(user=user_id).all()
    for image in images:
        image.image = base64.b64encode(image.image).decode('utf-8')
    return render_template('process/captured.html', images=images)