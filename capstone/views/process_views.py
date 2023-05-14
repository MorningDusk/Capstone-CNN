from datetime import datetime
import io

from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.utils import redirect
import requests
import pytz

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
    url = 'http://7d5b-34-143-145-123.ngrok-free.app/process'
    response = requests.post(url, json=data)

    if response.status_code == 200:
        return response.json()['result']
    else:
        return None


@bp.route('/img', methods=('GET', 'POST'))
def img():
    form = ImageForm()
    if request.method == 'POST':
        file = request.files['image-file']
        url = request.form['image-url']
        if file:
            user_id = session.get('user_id')
            time_now = datetime.now(pytz.timezone('Asia/Seoul'))
            image = Image(user=user_id, image=file.read(), date=time_now)
            db.session.add(image)
            db.session.commit()

            return redirect(url_for('main.index'))
        elif len(url) != 0:
            if is_image_url(url):
                response = requests.get(url)
                if response.status_code == 200:
                    user_id = session.get('user_id')
                    time_now = datetime.now(pytz.timezone('Asia/Seoul'))
                    image = Image(user=user_id, image=response.content, date=time_now)
                    db.session.add(image)
                    db.session.commit()

                    return redirect(url_for('main.index'))
                else:
                    flash("오류가 발생했습니다.")
            else:
                flash("올바른 url을 입력해주세요.")
        else:
            flash("파일을 업로드해주세요.")
    return render_template('process/img.html', form=form)

@bp.route('/cam', methods=('GET', 'POST'))
def cam():
    return render_template('process/cam.html')

@bp.route('/result', methods=('GET', 'POST'))
def result():
    return render_template('process/result.html')

@bp.route('/save', methods=('GET', 'POST'))
def save_image():
    user_id = session.get('user_id')
    time_now = datetime.now(pytz.timezone('Asia/Seoul'))
    data = request.files['image'].read()
    image = Image(user=user_id, image=data, date=time_now)
    db.session.add(image)
    db.session.commit()
    return redirect(url_for('main.index'))