from flask import Blueprint, url_for, session, render_template
from werkzeug.utils import redirect

from pybo import db
from pybo.models import User

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/select', methods=('GET', 'POST'))
def select():
    return render_template('main.html')

@bp.route('/')
def index():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('auth.login'))
    else:
        return redirect(url_for('main.select'))

