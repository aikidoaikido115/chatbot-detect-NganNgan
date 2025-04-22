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

from app.domain.AWS.interfaces import (
    S3ImageUploaderInterface
)

from util.flex import flex_select_enhance, flex_output
from typing import Optional, List

class UserService:
    def __init__(self, user_repo: UserRepositoryInterface):
        self.user_repo = user_repo

    async def create_user(self,id: str) -> Optional[User]:
        if await self.user_repo.find_by_id(id):
            print("Username ซ้ำข้ามขั้นตอนนี้")
            return None
        
        new_user = User(id=id)
        return await self.user_repo.save(new_user)

    async def get_users(self) -> List[User]:
        users = await self.user_repo.get_all()

        return [user.to_dict() for user in users]
    
    async def get_user_by_id(self, id: str) -> Optional[User]:
        user = await self.user_repo.get_by_id(id)
        return user

class CommandService:
    def __init__(self, command_repo: CommandRepositoryInterface):
        self.command_repo = command_repo

    async def create_command(self,user_id: str, name: str) -> Optional[Command]:
        print("ก่อนเข้า if")
        if await self.command_repo.find_by_user_id(user_id):
            deleted_all_user_command = await self.command_repo.delete_all_user_command(user_id)
            print(deleted_all_user_command)
        
        new_command = Command(user_id=user_id, name=name)
        return await self.command_repo.save(new_command)

    async def get_commands(self) -> List[Command]:
        commands = await self.command_repo.get_all()

        return [command.to_dict() for command in commands]
    
    async def get_command_by_user_id(self, user_id: str) -> Command:
        command = await self.command_repo.find_by_user_id(user_id)
        return command.to_dict()
    
class LineBotService(LineBotServiceInterface):
    def __init__(
        self, 
        messaging_adapter: LineMessagingInterface,
        image_storage: ImageStorageInterface,
        ocr: OcrInterface,
        enhance: ImageEnhanceInterface,
        bridge: ConnectLine2DatabaseInterface,
        aws_storage: S3ImageUploaderInterface
    ):
        self.messaging_adapter = messaging_adapter  # Inject Dependency
        self.image_storage = image_storage
        self.ocr = ocr
        self.enhance = enhance
        self.bridge = bridge
        self.aws_storage = aws_storage

        self.option_list = ["conv_sharpen", "unsharp_mask", "laplacian_sharpen", "gaussian_subtract"]

    async def handle_message(self, user_id: str, message: str) -> object:
        response = await self.bridge.post_requests_users(user_id)
        print(f"response สมัคร user มาละ {response}")
        reply_content = f"สวัสดีครับ ส่งข้อความทำไม กรุณาส่งรูปเข้ามาได้เลย\nลองพิมพ์คำว่า 'menu_select' ดูสิ 2"

        # Business logic สำหรับ Rich menu
        if message == "menu_select":
            reply_content = flex_select_enhance()
            print(reply_content)

        elif message in self.option_list:
            response = await self.bridge.post_requests_command(user_id=user_id, name=message)
            print(f"response สร้าง command มาแล้ว {response}")
            reply_content = f"ใช้ {message} แล้ว กรุณาส่งรูปเข้ามาได้เลยครับ"
        return reply_content
    
    async def handle_image(self, user_id: str, image_id: str) -> str:
        response = await self.bridge.post_requests_users(user_id)
        print(f"response มาละ {response}")

        image_content = await self.messaging_adapter.get_image_content(image_id)


        # self.image_storage.save_image(user_id, image_content)
        # OCR
        # print(image_content)

        
        enhance_method_obj = await self.bridge.get_requests_command_by_user_id(user_id)
        # กำหนดค่า default
        if enhance_method_obj == None:
            enhance_method_obj = {"name":"conv_sharpen"}

        print(f"ได้มาจาก database {enhance_method_obj}")
        if enhance_method_obj["name"] == self.option_list[0]:
            image_content = self.enhance.apply_conv_sharpen(image_content)

        elif enhance_method_obj["name"] == self.option_list[1]:
            print("มา unsharp")
            image_content = self.enhance.apply_unsharp_mask(image_content)
        
        elif enhance_method_obj["name"] == self.option_list[2]:
            print("มา lapla")
            image_content = self.enhance.apply_laplacian_sharpen(image_content)

        elif enhance_method_obj["name"] == self.option_list[3]:
            image_content = self.enhance.apply_gaussian_subtract(image_content)

        ocr_output = self.ocr.ocr(image_content)
        license_plate, province, _ = ocr_output.split("\n")

        image_url = await self.aws_storage.upload_image(image_content, folder="license_plate")

        # test_url = "https://detectngannganurl.s3.amazonaws.com/profile_pictures/11dbf2b2-d8d6-4aab-8f25-d4af21b97a82.png"
        return flex_output(image_url, license_plate, province)