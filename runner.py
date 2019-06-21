from googletrans import Translator
from bookprocessor import BookProcessor, ConversionEngine
import time
class ProgressCallback(object):

    def __init__(self):
        self._total = 0
        self._progress = 0


    def update_state(self, event, val=None):

        if event == "total":
            self._total = val
        elif event == "start":
            self._progress += 4.0/self._total
        elif event == "finish":
            self._progress += 94.0/self._total
        elif event == "complete":
            self._progress = 100


class SimpleConversionEngine(ConversionEngine):
    def __init__(self):
        self._translator = Translator(service_urls=['translate.google.cn'])
        self._times = 0
        self.chars_len = 0
    def convert(self, text):
        # conversion logic here
        #print(text)

        if len(text) == 0:
            return text

        self.chars_len = self.chars_len + len(text)
        print(self.chars_len)

        self._times = self._times + 1
        text = self._translator.translate(text, dest='en', src='ja').text
        print(text)
        time.sleep(5)
        #if  self._times % 100 == 0:
        #    print("[" + self._times +  "]sleep 30s...I dont want to be BANNED,pal")
        #    time.sleep(30)

        return text

if __name__ == "__main__":

    e = SimpleConversionEngine()
    u = BookProcessor(e, progress_callback=ProgressCallback())
    u.set_file("../input.epub", "../output.epub")
    u.convert()