# XPath Extractor
Finding it hard to paste html code into python variable to test xpath expressions?
Here is an app that will save you some time.

It uses scrapy.selector.XPathSelector, passes your html as text arg, applies xpath to it and extracts content. Simple as that.

Later we may add ability to pass a list of xpath expressions, each having fallback to the next one (in case previous returns nothing) and showing you which expression took effect.

## Instalation

    pip install -r requirements.txt

## Running the app

    python app.py
