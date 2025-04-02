from app.domain.interfaces import ImageStorageInterface
import os
import uuid


class ImageStorageAdapter(ImageStorageInterface):
    def __init__(self, storage_path: str = "downloads"):
        self.storage_path = storage_path
        os.makedirs(self.storage_path, exist_ok=True)

    def save_image(self, user_id: str, image_content: bytes) -> str:
        user_dir = os.path.join(self.storage_path, user_id)
        os.makedirs(user_dir, exist_ok=True)
        filename = f"{uuid.uuid4()}.jpg"
        filepath = os.path.join(user_dir, filename)
        with open(filepath, "wb") as f:
            f.write(image_content)
        return filepath