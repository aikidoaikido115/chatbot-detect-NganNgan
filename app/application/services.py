from app.domain.line.interfaces import (
    LineBotServiceInterface,
    LineMessagingInterface,
    ImageStorageInterface,
    OcrInterface,
    ImageEnhanceInterface
)
from app.domain.database.interfaces import (
    UserRepositoryInterface,
    CommandRepositoryInterface
)
from app.domain.database.models import (
    User,
    Command
)

# มันคือ requests.get หรือ post แบบ ABC
from app.domain.bridge.interfaces import (
    ConnectLine2DatabaseInterface
)

from util.flex import flex_select_enhance
from typing import Optional, List

class UserService:
    def __init__(self, user_repo: UserRepositoryInterface):
        self.user_repo = user_repo

    def create_user(self,id: str) -> Optional[User]:
        if self.user_repo.find_by_id(id):
            return None
        
        new_user = User(id=id)
        return self.user_repo.save(new_user)

    def get_users(self) -> List[User]:
        users = self.user_repo.get_all()

        return [user.to_dict() for user in users]

class CommandService:
    def __init__(self, command_repo: CommandRepositoryInterface):
        self.command_repo = command_repo

    def create_command(self,user_id: str, name: str) -> Optional[Command]:
        if self.command_repo.find_by_user_id(user_id):
            return None
        
        new_command = Command(user_id=user_id, name=name)
        return self.command_repo.save(new_command)

    def get_commands(self) -> List[Command]:
        commands = self.command_repo.get_all()

        return [commad.to_dict() for commad in commands]
    
class LineBotService(LineBotServiceInterface):
    def __init__(
        self, 
        messaging_adapter: LineMessagingInterface,
        image_storage: ImageStorageInterface,
        ocr: OcrInterface,
        enhance: ImageEnhanceInterface,
        bridge: ConnectLine2DatabaseInterface
    ):
        self.messaging_adapter = messaging_adapter  # Inject Dependency
        self.image_storage = image_storage
        self.ocr = ocr
        self.enhance = enhance
        self.bridge = bridge

        self.option_list = ["conv_sharpen", "unsharp_mask", "laplacian_sharpen", "gaussian_subtract"]

    def handle_message(self, user_id: str, message: str) -> object:
        self.bridge.post_requests_users(user_id) # ยิง requests post สร้าง user แบบถูกกฎของ hexagonal
        reply_content = f"สวัสดีครับ ส่งข้อความทำไม กรุณาส่งรูปเข้ามาได้เลย\nลองพิมพ์คำว่า 'menu_select' ดูสิ"

        # Business logic สำหรับ Rich menu
        if message == "menu_select":
            reply_content = flex_select_enhance()
            print(reply_content)

        elif message in self.option_list:
            # self.bridge.post_requests_command(message) # เซฟชื่อฟังก์ชัน image enhance ที่ user คนนั้นจะใช้
            reply_content = f"ใช้ {message} แล้ว กรุณาส่งรูปเข้ามาได้เลยครับ"
            # save ฟังชันล่าสุดลง database นี่คือวิธีที่จะทำให้จำข้อความที่ user เคยพิมพ์ได้
        return reply_content
    
    def handle_image(self, user_id: str, image_id: str) -> str:
        self.bridge.post_requests_users(user_id) # สร้าง user

        image_content = self.messaging_adapter.get_image_content(image_id)
        self.image_storage.save_image(user_id, image_content) # เปลี่ยนไปเก็บที่ database ก่อน
        # OCR
        # print(image_content)
        image_content = self.enhance.apply_conv_sharpen(image_content) # ต้องแก้โดยเอาฟังชันที่ user เลือกโดยอ้างอิงจาก database ที่ตั้งค่าเอาไว้ที่ handle_message
        reply_text = self.ocr.ocr(image_content)

        return reply_text