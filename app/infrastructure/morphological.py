from app.domain.line.interfaces import MorphologicalInterface
import imghdr
import cv2
import numpy as np
# import matplotlib.pyplot as plt

class MorphologicalAdapter(MorphologicalInterface):

    def _bytes_to_img(self, img_content):
        arr = np.frombuffer(img_content, dtype=np.uint8)
        img  = cv2.imdecode(arr, cv2.IMREAD_UNCHANGED)
        if img is None:
            raise ValueError("Decode image failed")
        return img.astype(np.uint8)
    
    def _img_to_bytes(self, img, ext):
        success, buf = cv2.imencode(f'.{ext}', img)
        if not success:
            raise ValueError("Encode image failed")
        return buf.tobytes()
    
    def _get_filetype(self, img_content):
        ftype = imghdr.what(None, h=img_content)
        if not ftype:
            raise ValueError("Unsupported / corrupted image")
        return ftype
    
    def _make_kernel(self, ksize):
        return cv2.getStructuringElement(cv2.MORPH_RECT, (ksize, ksize))
    
    def _preprocess(self, img):
        if len(img.shape) == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #ต้องเป็นขาวดำไม่งั้น dilate กับ erode จะสลับกัน
        return cv2.bitwise_not(img)

    def _postprocess(self, img):
        return cv2.bitwise_not(img)

    ############ util ส่วนตัวของ Morphological ############

    def morph_erosion(self, image_content: bytes, ksize: int = 3, iterations: int = 1) -> bytes:
        ext = self._get_filetype(image_content)
        img = self._bytes_to_img(image_content)
        processed = self._preprocess(img)
        kern = self._make_kernel(ksize)
        erode = cv2.erode(processed, kern, iterations=iterations)
        # result = self._postprocess(erode)
        print("morph_erosion")
        return self._img_to_bytes(erode, ext)

    def morph_dilation(self, image_content: bytes, ksize: int = 3, iterations: int = 1) -> bytes:
        ext = self._get_filetype(image_content)
        img = self._bytes_to_img(image_content)
        processed = self._preprocess(img)
        kern = self._make_kernel(ksize)
        dilate = cv2.dilate(processed, kern, iterations=iterations)
        # result = self._postprocess(dilate)
        print("morph_dilation")
        return self._img_to_bytes(dilate, ext)

    def morph_opening(self, image_content: bytes, ksize: int = 3, iterations: int = 1) -> bytes:
        ext = self._get_filetype(image_content)
        img = self._bytes_to_img(image_content)
        processed = self._preprocess(img)
        kern = self._make_kernel(ksize)
        open = cv2.morphologyEx(processed, cv2.MORPH_OPEN, kern, iterations=iterations)
        # result = self._postprocess(open)
        print("morph_opening")
        return self._img_to_bytes(open, ext)

    def morph_closing(self, image_content: bytes, ksize: int = 3, iterations: int = 1) -> bytes:
        ext = self._get_filetype(image_content)
        img = self._bytes_to_img(image_content)
        processed = self._preprocess(img)
        kern = self._make_kernel(ksize)
        close = cv2.morphologyEx(processed, cv2.MORPH_CLOSE, kern, iterations=iterations)
        # result = self._postprocess(close)
        print("morph_closing")
        return self._img_to_bytes(close, ext)
