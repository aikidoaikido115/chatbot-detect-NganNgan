from abc import ABC, abstractmethod

class S3ImageUploaderInterface(ABC):
    @abstractmethod
    async def upload_image(self, image_bytes: bytes, folder: str, content_type=None) -> str:
        pass
