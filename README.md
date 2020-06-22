# ja-epub-translator
Translate japanese epub into english one.
very early stage version.

Change log
--
* v0.11 Add new translator, now support jp-cn translation. Code from `http://github.com/neverneverendup/Translator`
* v0.1  Initial version

Demonstration 
--
- Origin epub

![avatar](res/ja.jpg)

- Translated epub

![avatar](res/enja.jpg)


Requirement
--
```
pip install BeautifulSoup
pip install googletrans
```


Usage
--
python runner.py

Limitation
--
- Only supports the epub files coverted by [Calibre](https://calibre-ebook.com/) for now.
- Only translate one sentence per 5 second. That is [limited](https://github.com/ssut/py-googletrans/issues/121) by googletrans' API. Your IP may be banned if your request is submitted too fast.

More details TBA.
--
