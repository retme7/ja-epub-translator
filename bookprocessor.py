from BeautifulSoup import BeautifulSoup, NavigableString,Tag
from zipfile import ZipFile, ZIP_DEFLATED
import re
import shutil
from threadedconvert import ThreadedConvert
import sys
import time

class ConversionEngine(object):

    def convert(self, text):
        raise NotImplementedError("Conversion Engine must be subclassed")


class BookProcessor(object):

    def __init__(self, conversion_engine, progress_callback=None):
        self._conversion_engine = conversion_engine
        self._callback = progress_callback

    def set_file(self, src_file, dest_file=None):
        self._filepath = src_file
        self._destfile = dest_file

    def get_html_files_ref(self):
        htmlfiles = []

        with ZipFile(self._filepath, 'r') as f:
            foo = f.open('META-INF/container.xml')
            soup = BeautifulSoup(foo)
            foo.close()
            contentfile = dict(soup.find('rootfile').attrs)['full-path']
            soup.close()

            root = re.sub(r'[^/]*(.opf)', '', contentfile)

            foo = f.open(contentfile)
            soup = BeautifulSoup(foo)
            for item in soup.findAll('item'):
                itemdict = dict(item.attrs)
                if itemdict['href'].endswith('html'):
                    htmlfiles.append(root + itemdict['href'])

            foo.close()
            soup.close()
            f.close()

        return htmlfiles

    def get_converted_html(self, soup):

        #remote note for Chinese charactors: Tag <rt>
        #for nstring in soup.findAll( {'rt' : True}):
        #    nstring.extract()

        #remote tag <ruby> but keep the char inside
        for pTag in soup.findAll( {'p' : True}):
            #only support calibre-converted ebook, for NOW
            if pTag['class'] != 'calibre':
                continue
            new_content = u''
            for content in pTag.contents:
                if type(content) is NavigableString:
                    new_content = new_content + content
                elif content.name == "ruby" :
                    for ruby_char in content.contents:
                        #ignore <rt>
                        if type(ruby_char) is NavigableString:
                            new_content = new_content + ruby_char
            

            #print(new_content)
            #continue
            # new_content is a sentence. send it to Google translate
            try:
                en_text = self._conversion_engine.convert(new_content)        
            except Exception,err:
                en_text = "TRANSLATE ERROR"
                print(err)
                print(new_content)
 
            if len(new_content) >0:
                br1 = Tag(soup, "br")
                br2 = Tag(soup, "br")
                idx = len(pTag.contents)
                pTag.insert(idx, br1)
                pTag.insert(idx+1, NavigableString("&emsp;" + en_text))
                pTag.insert(idx+2, br2)

            #DEBUG for once
            #if len(new_content) >0:
            #    break


        return str(soup)

    def convert(self):

        if self._destfile is None or self._filepath == self._destfile:
            self._destfile = self._filepath
        else:
            shutil.copyfile(self._filepath, self._destfile)

        htmls = self.get_html_files_ref()

        if self._callback:
            self._callback.update_state("total", len(htmls))

        with ZipFile(self._destfile, 'a', ZIP_DEFLATED) as f:
            threads = []
            for item in htmls:
                #only for calibre epub
                if item.find("text/") == -1:
                    continue
                t = ThreadedConvert(self, item, f, self._callback)
                t.start()
                #wait for finish. Do not use multi thread feature, OR your ip will be BANNED !
                t.join()

                #threads.append(t)

            #for t in threads:
            #    t.join()

            f.close()

        if self._callback:
            self._callback.update_state("complete")