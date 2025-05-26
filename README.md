# สวัสดีครับสมาชิกชมรมทุกท่าน

## Hexagonal Architecture: Line Chatbot YOLO + OCR + image enhance
---

### 1. **การ Clone โปรเจกต์**

เปิด Command Prompt (Windows) หรือ Terminal (Mac/Linux) แล้วรันคำสั่งด้านล่าง:
```bash
git clone https://github.com/aikidoaikido115/chatbot-detect-NganNgan.git
```

---

### 2. **ตั้งค่า Virtual Environment**

สร้าง Virtual Environment เพื่อแยก dependencies ของโปรเจกต์:
```bash
python -m venv venv
```
เปิดใช้งาน Virtual Environment:
- **Windows**:
  ```bash
  venv\Scripts\activate
  ```
- **Mac/Linux**:
  ```bash
  source venv/bin/activate
  ```

---

### 3. **ติดตั้ง Dependencies**

ติดตั้งไลบรารีที่จำเป็นทั้งหมดจากไฟล์ `requirements.txt`:
```bash
pip install -r requirements.txt
```

---

### 4. **ตั้งค่า Environment Variables**

สร้างไฟล์ `.env` เพิ่มที่ root
```plaintext
GOOGLE_API_KEY=ความลับสุดยอด1
DATABASE_URL=ความลับสุดยอด2

BUCKET_NAME = ความลับสุดยอด3
REGION_NAME = ความลับสุดยอด4
AWS_ACCESS_KEY = ความลับสุดยอด_ป่าอเมซอน1
AWS_SECRET_KEY = ความลับสุดยอด_ป่าอเมซอน2

LINE_ACCESS_TOKEN=ความลับสุดยอด5
```

---

### **5. การรันฐานข้อมูล**

```bash
docker-compose up -d
```

---

### **6. การรันแอปพลิเคชัน**

```bash
uvicorn app.main:app --reload
```

---

### **7. ใช้ ngrok ต่อกับ line webhook**

```bash
ngrok http 8000
```
