from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import base64
import httpx

import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')


image_url = 'test.png'

try:
    # โหลดรูปจาก url
    image_data = base64.b64encode(httpx.get(image_url).content).decode("utf-8")
except:
    #ไม่ใช่ url ก็ลองโหลดแบบ local
    with open(image_url, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode("utf-8")

#HumanMessage สามารถแนบรูปได้
message = HumanMessage(
    content=[
        {"type": "text", "text": "Extract the text from this image and return it as plain text."},
        {
            "type": "image_url",
            "image_url": f"data:image/png;base64,{image_data}",
        },
    ]
)


model = ChatGoogleGenerativeAI(model="gemini-2.0-flash")


response = model([message])

print(response.content)
