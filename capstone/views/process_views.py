import io

from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.utils import redirect
import requests
from PIL import Image as Img

from capstone import db
from capstone.forms import ImageForm
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

@bp.route('/img', methods=('GET', 'POST'))
def img():
    form = ImageForm()
    if request.method == 'POST':
        file = request.files['image-file']
        url = request.form['image-url']
        if file:
            image = Image(image=file.read())
            db.session.add(image)
            db.session.commit()
            return redirect(url_for('main.index'))
        elif len(url) != 0:
            if is_image_url(url):
                response = requests.get(url)
                if response.status_code == 200:
                    image = Image(image=response.content)
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