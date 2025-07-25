from app.domain.line.interfaces import OcrInterface
import base64
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import imghdr
import os
from time import sleep
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

class OcrAdapter(OcrInterface):

    def ocr(self, image_content: bytes) -> str:
        
        file_type = imghdr.what(None, h=image_content)
        print(f"นี่คือ filetype ocr {file_type}")

        if not file_type:
            raise ValueError("Unsupported or corrupted image format")
        

        base64_image = base64.b64encode(image_content).decode("utf-8")

        message = HumanMessage(
            content=[
                {
                    "type": "text",
                    "text": (
                        "You are an expert at extracting text from Thai license plate images, even under challenging conditions "
                        "such as blur, glare, tilt, or partial obstruction.\n\n"
                        "Please extract and return the following information from the image:\n"
                        "- The license plate number (e.g. 1กข 1234)\n"
                        "- The province written on the plate (in Thai)\n\n"
                        "Return the result as plain text only in this format:\n"
                        "<license plate number>\n"
                        "<province in Thai>\n\n"
                        "If any part is unclear, make your best guess. Return only the most prominent license plate."
                        "If no license plate is found or the image is not related to a vehicle license plate, simply respond with:\n"
                        "-1\n"
                        "-1\n\n"
                    )
                },
                {
                    "type": "image_url",
                    "image_url": f"data:image/{file_type};base64,{base64_image}",
                },
            ]
)
        model = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
        response = model.invoke([message])
        sleep(0.25)
        return str(response.content)