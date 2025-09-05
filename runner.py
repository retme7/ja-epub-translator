from googletrans import Translator
from bookprocessor import BookProcessor, ConversionEngine
from tencent import TencentTrans
from aitranslator import OpenAITrans
import time
import argparse

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


class GoogleConversionEngine(ConversionEngine):
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


class OpenAIConversionEngine(ConversionEngine):
    def __init__(self):
        self._translator = OpenAITrans()
        self._translator.tolang = 'Simplified Chinese'
        self._times = 0
        self.chars_len = 0
        return 
    def convert(self, text):
        if len(text) <= 2:
            return text
        self.chars_len = self.chars_len + len(text)
        print(self.chars_len)
        self._times = self._times + 1
        
        # Call the actual translation method
        try:
            result = self._translator.get_trans_result(text)
            print(result)
            return result
        except Exception as err:
            print(f"Translation error: {err}")
            return "TRANSLATE ERROR"


class TencentConversionEngine(ConversionEngine):
    def __init__(self):
        self._translator = TencentTrans()
        self._translator.tolang = 'Simplified Chinese'
        self._times = 0
        self.chars_len = 0
        return 
    def convert(self, text):
        if len(text) == 0:
            return text

        self.chars_len = self.chars_len + len(text)
        print(self.chars_len)

        self._times = self._times + 1

        print(text)
        t = self._translator.get_trans_result(text)

        print(t)
        #time.sleep(5)

        return t

if __name__ == "__main__":
    
    #e = GoogleConversionEngine()
    #e = TencentConversionEngine()
    e = OpenAIConversionEngine()
    u = BookProcessor(e, progress_callback=ProgressCallback())

    parser = argparse.ArgumentParser(description='exp03')
    parser.add_argument('--input', type=str, required=True, help='input epub file')
    parser.add_argument('--output', type=str, required=False,default="output.epub", help='output epub file')
    args = parser.parse_args()
    input_path = args.input
    output_path = args.output
    
    u.set_file(input_path, output_path)
    u.convert()
