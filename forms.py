import re

import requests
from wtforms.form import Form
from wtforms.fields import TextAreaField, StringField
from wtforms import validators
from scrapy.selector import Selector


class XPathExtractorForm(Form):
    xpath = StringField(validators=[validators.required()])
    html = TextAreaField(validators=[validators.required()])

    def resolve(self):
        html = self.data['html']
        xpath = self.data['xpath']
        if re.match('http.*://.*\..*', html):
            resp = requests.get(self.data['html'].strip())
            if resp.status_code == 200:
                html = resp.content
        return [x for x in Selector(text=html).xpath(xpath).extract() if x.strip()]
