# -*- coding: utf-8 -*-
import re

import requests
from wtforms.form import Form
from wtforms.fields import TextAreaField, StringField
from wtforms import validators
from scrapy.selector import Selector

from config import USER_AGENT

from utils import xpath
xpath.setup()


class XPathExtractorForm(Form):
    xpath = StringField("XPATH", validators=[validators.required()])
    html = TextAreaField("HTML or URL", validators=[validators.required()])

    def resolve(self):
        html = self.data['html']
        xpath = self.data['xpath']
        if re.match('http.*://.*\..*', html):
            headers = {
                'User-Agent': USER_AGENT
            }
            resp = requests.get(self.data['html'].strip(), headers=headers)
            if resp.status_code == 200:
                html = resp.content.decode(resp.encoding)
        return [x for x in Selector(text=html).xpath(xpath).extract() if x.strip()], html, xpath
