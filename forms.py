from wtforms.form import Form
from wtforms.fields import TextAreaField, StringField
from wtforms import validators

from scrapy.selector import XPathSelector


class XPathExtractorForm(Form):
    xpath = StringField(validators=[validators.required()])
    html = TextAreaField(validators=[validators.required()])

    def resolve(self):
        sel = XPathSelector(text=self.data['html'])
        return sel.xpath(self.data['xpath']).extract()
