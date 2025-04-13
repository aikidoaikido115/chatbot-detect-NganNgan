# สวัสดีครับสมาชิกชมรมทุกท่าน

## Hexagonal Architecture: Line Chatbot YOLO + OCR + image enhance
---

### 2. **การ Clone โปรเจกต์**

เปิด Command Prompt (Windows) หรือ Terminal (Mac/Linux) แล้วรันคำสั่งด้านล่าง:
```bash
git clone https://github.com/aikidoaikido115/chatbot-detect-NganNgan.git
```

---

### 3. **ตั้งค่า Virtual Environment**

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

### 4. **ติดตั้ง Dependencies**

ติดตั้งไลบรารีที่จำเป็นทั้งหมดจากไฟล์ `requirements.txt`:
```bash
pip install -r requirements.txt
```

---

### 5. **ตั้งค่า Environment Variables**

สร้างไฟล์ `.env` เพิ่มที่ root
```plaintext
GOOGLE_API_KEY=your_api_key
LINE_ACCESS_TOKEN=your_token
```

---

### **6. การรันฐานข้อมูล**

```bash
docker-compose up -d
```

---

### **7. การรันแอปพลิเคชัน**

```bash
uvicorn app.main:app --reload
```
