from app.domain.interfaces import OcrInterface
import base64
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import imghdr
import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

class OcrAdapter(OcrInterface):

    def ocr(self, image_content: bytes) -> str:
        
        file_type = imghdr.what(None, h=image_content)
        print(f"นี่คือ filetype {file_type}")

        if not file_type:
            raise ValueError("Unsupported or corrupted image format")
        

        base64_image = base64.b64encode(image_content).decode("utf-8")

        message = HumanMessage(
            content=[
                {"type": "text", "text": "Extract the text from this image and return it as plain text."},
                {
                    "type": "image_url",
                    "image_url": f"data:image/{file_type};base64,{base64_image}",
                },
            ]
        )
        model = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
        response = model.invoke([message])
        return str(response.content)