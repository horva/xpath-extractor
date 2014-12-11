# -*- coding: utf-8 -*-
import re

import requests
from wtforms.form import Form
from wtforms.fields import TextAreaField, StringField, HiddenField
from wtforms import validators
from scrapy.selector import Selector

from config import USER_AGENT

from utils import xpath
xpath.setup()


class XPathExtractorForm(Form):
    xpath = StringField("XPATH", validators=[validators.required()])
    html = TextAreaField("HTML or URL", validators=[validators.required()])
    subxpath = StringField("Sub-XPATH", validators=[validators.optional()])
    url = HiddenField()

    def resolve(self):
        html = self.data['html']
        xpath = self.data['xpath']
        subxpath = self.data['subxpath']
        url = self.data['url']
        if re.match('http.*://.*\..*', html):
            headers = {
                'User-Agent': USER_AGENT
            }
            resp = requests.get(html.strip(), headers=headers)
            if resp.status_code == 200:
                url = html
                html = resp.content.decode(resp.encoding)

        if subxpath:
            result = [(i, sel.xpath(subxpath).extract())
                      for (i, sel) in enumerate(Selector(text=html).xpath(xpath), 1)]
        else:
            result = [x for x in Selector(text=html).xpath(xpath).extract() if x.strip()]

        return (result, html, url, xpath, subxpath)
