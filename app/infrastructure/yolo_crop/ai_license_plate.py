from app.domain.yolo_crop.interfaces import YoloCropInterface
import cv2
import numpy as np
from ultralytics import YOLO
from typing import Tuple, List

model = YOLO('app/infrastructure/yolo_crop/license_plate_detector.pt')

class YoloCropAdapter(YoloCropInterface):
    def crop(
        self,
        image_bytes: bytes,
        conf_threshold: float = 0.5,
        imgsz: int = 640
    ) -> Tuple[bytes, List[bytes]]:
        

        print(f"เข้ามาใน YoloCropAdapter {image_bytes[0:30]}")
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("ไม่สามารถ decode ภาพจาก bytes ได้")

        # run detection
        results = model.predict(source=img, imgsz=imgsz, conf=conf_threshold, verbose=False)
        boxes = results[0].boxes.xyxy
        classes = results[0].boxes.cls
        names = results[0].names

        cropped_bytes: List[bytes] = []
        # วาดกรอบและคร็อป
        for box, cls in zip(boxes, classes):
            x1, y1, x2, y2 = map(int, box)
            label = names[int(cls)]
            if label == 'license_plate':
                # กรอบสีเขียว
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(
                    img, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2
                )
                # คร็อปและปรับขนาด
                plate = img[y1:y2, x1:x2]
                plate = cv2.resize(plate, (300, 150))
                # encode → bytes
                success, buf = cv2.imencode('.jpg', plate)
                if success:
                    cropped_bytes.append(buf.tobytes())

        # encode ภาพหลักที่วาดกรอบแล้ว → bytes
        success, out_buf = cv2.imencode('.jpg', img)
        if not success:
            raise RuntimeError("ไม่สามารถ encode ภาพผลลัพธ์ได้")
        annotated_bytes = out_buf.tobytes()

        print(f"ได้ภาพหลัก (annotated) ขนาด {len(annotated_bytes)} bytes")
        for i, p in enumerate(cropped_bytes):
            print(f"👉 plate #{i} : {len(p)} bytes")

        return annotated_bytes, cropped_bytes