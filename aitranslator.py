from pydantic import BaseModel
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")


class OpenAITrans(object):
    def __init__(self):
        self.tolang = 'Simplified Chinese'
        return 
    def get_trans_result(self, text):
        try:
            target_lang = self.tolang
            response = client.chat.completions.create(
                temperature=0,
                model="huihui_ai/hunyuan-mt-abliterated",
                messages=[
                    {"role": "system", "content": f"You are a translator. Translate the user's text into {self.tolang}."},
                    {"role": "user", "content": text},
                ],
             )

            text = response.choices[0].message.content.strip()

        except Exception as e:
            print(f"Error: {e}")

        return text