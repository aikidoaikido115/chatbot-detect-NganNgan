def str_to_bool(s):
    if s.lower() == "true":
        return True
    elif s.lower() == "false":
        return False
    else:
        print("ไม่ใช่ bool แปลงไม่ได้")
        return None