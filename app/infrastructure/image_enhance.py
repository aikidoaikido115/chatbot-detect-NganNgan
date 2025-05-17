from app.domain.line.interfaces import ImageEnhanceInterface
import imghdr
import cv2
import numpy as np
# import matplotlib.pyplot as plt

class ImageEnhanceAdapter(ImageEnhanceInterface):

    # high-pass convolution
    def apply_conv_sharpen(self, image_content: bytes) -> bytes:

        file_type = imghdr.what(None, h=image_content)
        print(f"นี่คือ filetype ของ apply_conv_sharpen {file_type}")

        if not file_type:
            raise ValueError("Unsupported or corrupted image format")
        
        
        img_array = np.frombuffer(image_content, dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_UNCHANGED)
        
        # สร้าง kernel สำหรับเพิ่มความคมชัด
        kernel = np.array([[0, -1, 0],
                        [-1, 5, -1],
                        [0, -1, 0]])
        sharpened = cv2.filter2D(img, -1, kernel)
        
        _, buffer = cv2.imencode(f'.{file_type}', sharpened)
        print("รูปถูก apply_conv_sharpen เรียบร้อยแล้ว")

        # เช็คว่ารูปถูก enhance จริงไหม
        # if len(sharpened.shape) == 3 and sharpened.shape[2] == 3:
        #     sharpened_rgb = cv2.cvtColor(sharpened, cv2.COLOR_BGR2RGB)
        #     plt.imshow(sharpened_rgb)
        # else:
        #     plt.imshow(sharpened, cmap='gray')
        # plt.title("Sharpened Image")
        # plt.axis('off')
        # plt.show()

        return buffer.tobytes()
    def apply_unsharp_mask(self, image_content: bytes, sigma=1.0, strength=0.7) -> bytes:

        file_type = imghdr.what(None, h=image_content)
        print(f"นี่คือ filetype ของ apply_unsharp_mask {file_type}")

        if not file_type:
            raise ValueError("Unsupported or corrupted image format")
        
        img_array = np.frombuffer(image_content, dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        
        blurred = cv2.GaussianBlur(img, (0,0), sigma)
        mask = cv2.addWeighted(img, 1.0, blurred, -1.0, 0)
        sharpened = cv2.addWeighted(img, 1.0, mask, strength, 0)
        
        _, buffer = cv2.imencode(f'.{file_type}', sharpened)
        print("รูปถูก apply_unsharp_mask เรียบร้อยแล้ว")

        return buffer.tobytes()
    

    def apply_laplacian_sharpen(self, image_content: bytes, alpha=0.3) -> bytes:

        file_type = imghdr.what(None, h=image_content)
        print(f"นี่คือ filetype ของ apply_laplacian_sharpen {file_type}")

        if not file_type:
            raise ValueError("Unsupported or corrupted image format")
        
        img_array = np.frombuffer(image_content, dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        
        laplacian = cv2.Laplacian(img, cv2.CV_32F)
        sharpened = cv2.convertScaleAbs(img - alpha*laplacian)
        
        _, buffer = cv2.imencode(f'.{file_type}', sharpened)
        print("รูปถูก apply_laplacian_sharpen เรียบร้อยแล้ว")

        return buffer.tobytes()
    
    def apply_gaussian_subtract(self, image_content: bytes, ksize=5) -> bytes:

        file_type = imghdr.what(None, h=image_content)
        print(f"นี่คือ filetype ของ apply_gaussian_subtract {file_type}")
        if not file_type:
            raise ValueError("Unsupported or corrupted image format")
        
        img_array = np.frombuffer(image_content, dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        
        blurred = cv2.GaussianBlur(img, (ksize,ksize), 0)
        sharpened = cv2.addWeighted(img, 1.5, blurred, -0.5, 0)

        _, buffer = cv2.imencode(f'.{file_type}', sharpened)
        print("รูปถูก apply_gaussian_subtract เรียบร้อยแล้ว")
    
        return buffer.tobytes()