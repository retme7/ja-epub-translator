
import threading
from BeautifulSoup import BeautifulSoup


class ThreadedConvert(threading.Thread):

    def __init__(self, processor, item, filex, callback=None):
        super(ThreadedConvert, self).__init__()
        self._item = item
        self._file = filex
        self._processor = processor
        self._callback = callback

    def run(self):
        if self._callback:
            self._callback.update_state("start")
        itemhtml = self._file.open(str(self._item))
        soup = BeautifulSoup(itemhtml)
        converted = self._processor.get_converted_html(soup)
        self._file.writestr(self._item, converted)
        soup.close()
        itemhtml.close()
        if self._callback:
            self._callback.update_state("finish")
