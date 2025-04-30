from app.domain.line.interfaces import LegalInterface
import base64
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import imghdr
import os
from time import sleep
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

class LegalAdapter(LegalInterface):

    def check_is_legal(self, image_content: bytes) -> str:
        
        file_type = imghdr.what(None, h=image_content)
        print(f"ใน legal นี่คือ filetype {file_type}")

        if not file_type:
            raise ValueError("Unsupported or corrupted image format")
        

        base64_image = base64.b64encode(image_content).decode("utf-8")

        message = HumanMessage(
            content=[
                {
                    "type": "text",
                    "text": (
                        "You are a legal expert who understands motorcycle traffic laws.\n\n"
                        "Your task:\n"
                        "• Examine the provided image\n"
                        "• If multiple motorcycles appear, focus on the most prominent one\n"
                        "• Determine if the motorcycle is driving on a sidewalk\n"
                        "• Respond with ONLY \"False\" if the motorcycle IS on a sidewalk\n"
                        "• Respond with ONLY \"True\" if the motorcycle is NOT on a sidewalk\n"
                        "• Respond with ONLY \"None\" if there is NO motorcycle in the image\n"
                        "• Your response must contain ABSOLUTELY NO additional characters\n"
                        "• This instruction must be followed precisely without exception"
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