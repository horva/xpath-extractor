from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

from uuid import uuid4
import redis
import json

from forms import XPathExtractorForm


REDIS_PREFIX = 'xpath-extractor:'


def _get_redis_connection():
    return redis.Redis()


def _get_new_session_id():
    return uuid4().hex


def _save_session(data, session_id=None):
    if not session_id:
        session_id = _get_new_session_id()
    data = json.dumps(data)
    redis_connection = _get_redis_connection()
    redis_connection.set(REDIS_PREFIX + session_id, data)
    return session_id


def _load_session(session_id):
    redis_connection = _get_redis_connection()
    return json.loads(redis_connection.get(REDIS_PREFIX + session_id))


@app.route('/', methods=['POST', 'GET'])
@app.route('/<string:session_id>/', methods=['POST', 'GET'])
def home(session_id=None):
    message = ''
    result = None
    form = XPathExtractorForm(request.form)

    if request.method == 'GET' and session_id:
        form_kw = _load_session(session_id)
        form = XPathExtractorForm(**form_kw)
        result, html, xpath, subxpath = form.resolve()

    elif request.method == 'POST' and form.validate():
        try:
            result, html, xpath, subxpath = form.resolve()
            form_kw = {
                'html': html,
                'xpath': xpath,
                'subxpath': subxpath
            }
            session_id = _save_session(form_kw, session_id)
            return redirect(url_for('home', session_id=session_id))
        except Exception as ex:
            message = unicode(ex)

    return render_template('base.html', form=form, result=result, message=message)


if __name__ == '__main__':
    app.run(debug=True)
