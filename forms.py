import re

import requests
from wtforms.form import Form
from wtforms.fields import TextAreaField, StringField
from wtforms import validators
from scrapy.selector import XPathSelector


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
        sel = XPathSelector(text=html)
        return [x for x in sel.xpath(xpath).extract() if x.strip()]
