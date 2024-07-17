from datetime import datetime
from openai import OpenAI
import json



class GPT_Model:
    def __init__(self, app) -> None:
        self.api_key = app.config['OPENAI_API_KEY']
        self.base_url = app.config['OPENAI_BASE_URL']
        self.client = OpenAI(api_key=self.api_key)
        
    def ask_image(self, image_url: str, knowledge_base: dict) -> str:
        """
        根据图片描述内容
        :param image_url: 图片地址
        :param knowledge_base: 知识库
        :return: 描述内容
        """
        print(image_url)
        completion = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "你是一个私人定制化的AI助手，接下来你将收到一个知识库，这个知识库中包含了我近五分钟内所说的话和对所拍摄照片的理解。请根据这个知识库用词条化的语言不超过十个词语解释我接下来拍到的照片。",
                        }
                    ],
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "这是一个JSON形式的知识库，你可以根据这个知识库来回答我接下来拍到的照片是什么：\n" + json.dumps(knowledge_base, indent=4)
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": image_url}
                        }
                    ]
                }
            ]
        )
        response = completion.choices[0].message.content
        return response