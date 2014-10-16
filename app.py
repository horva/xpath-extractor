from flask import Flask, render_template, request
app = Flask(__name__)


from forms import XPathExtractorForm


@app.route('/', methods=['POST', 'GET'])
def home():
    result = None
    form = XPathExtractorForm(request.form)
    if request.method == 'POST' and form.validate():
        result = form.resolve()
    return render_template('base.html', form=form, result=result)


if __name__ == '__main__':
    app.run(debug=True)
