from abc import ABC, abstractmethod
from typing import Tuple, List

class YoloCropInterface(ABC):
    @abstractmethod
    async def crop(self, image_bytes: bytes) -> Tuple[bytes, List[bytes]]:
        pass
