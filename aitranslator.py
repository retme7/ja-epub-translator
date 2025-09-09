from pydantic import BaseModel
from openai import OpenAI
import aiconfig
client = OpenAI(base_url=aiconfig.OPEN_AI_BASE_URL, api_key=aiconfig.OPEN_AI_API_KEY)
#client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

class OpenAITrans(object):
    def __init__(self):
        self.tolang = 'Simplified Chinese'
        return 
    def get_trans_result(self, text):
        try:
            target_lang = self.tolang
            response = client.chat.completions.create(
                temperature=0,
                #model="huihui_ai/hunyuan-mt-abliterated",
                model=aiconfig.OPEN_AI_MODEL,
                messages=[
                    #{"role": "system", "content": f"You are a translator. Translate the user's text into {self.tolang}."},
                    {"role": "system", "content": f"You are a translator.Translate the user's text into fluent, elegant {self.tolang} with literary flair. Make sure the translation captures the tone, atmosphere, and emotions of the original text, while still reading naturally as if it were originally written in {self.tolang}. Only output the translation, do not explain."},
                    {"role": "user", "content": text},
                ],
             )

            text = response.choices[0].message.content.strip()

        except Exception as e:
            print(f"Error: {e}")

        return text

class OpenAITest(object):
    def __init__(self):
        self.tolang = 'Simplified Chinese'
        return 
    def get_trans_result(self, text):
        with open('test.txt', 'r') as f:
            text = f.read()
        return text