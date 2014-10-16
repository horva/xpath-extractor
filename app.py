from flask import Flask, render_template, request
app = Flask(__name__)


from forms import XPathExtractorForm


@app.route('/', methods=['POST', 'GET'])
def home():
    message = ''
    result = None
    form = XPathExtractorForm(request.form)
    if request.method == 'POST' and form.validate():
        try:
            result = form.resolve()
            message = 'Found following results:' if result else 'No results.'
        except Exception as ex:
            message = str(ex)
    return render_template('base.html', form=form, result=result,
        message=message)


if __name__ == '__main__':
    app.run(debug=True)
