from flask import Blueprint, url_for, session, render_template

bp = Blueprint('process', __name__, url_prefix='/process')

@bp.route('/img', methods=('GET', 'POST'))
def img():
    return render_template('process/img.html')

@bp.route('/cam', methods=('GET', 'POST'))
def cam():
    return render_template('process/cam.html')