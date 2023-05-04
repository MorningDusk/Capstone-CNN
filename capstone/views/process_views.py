from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.utils import redirect

from capstone import db
from capstone.forms import ImageForm
from capstone.models import Image

bp = Blueprint('process', __name__, url_prefix='/process')

@bp.route('/img', methods=('GET', 'POST'))
def img():
    form = ImageForm()
    if request.method == 'POST':
        file = request.files['image-file']
        error = None
        if file:
            image = Image(image=file.read())
            db.session.add(image)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash("파일을 업로드해주세요.")
    return render_template('process/img.html', form=form)

@bp.route('/cam', methods=('GET', 'POST'))
def cam():
    return render_template('process/cam.html')