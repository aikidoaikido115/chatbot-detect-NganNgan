def flex_select_enhance():
    return {
  "type": "bubble",
  "direction": "ltr",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "เลือกวิธีการปรับปรุงรูปภาพ",
            "weight": "bold",
            "size": "lg",
            "align": "center",
            "gravity": "center",
            "margin": "md",
            "contents": []
          },
          {
            "type": "separator",
            "margin": "lg",
            "color": "#B7B7B7FF"
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "lg",
            "contents": [
              {
                "type": "button",
                "action": {
                  "type": "message",
                  "label": "conv_sharpen",
                  "text": "conv_sharpen"
                },
                "color": "#1E90FF",
                "gravity": "center"
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "lg",
            "contents": [
              {
                "type": "button",
                "action": {
                  "type": "message",
                  "label": "unsharp_mask",
                  "text": "unsharp_mask"
                },
                "color": "#1E90FF",
                "gravity": "center"
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "lg",
            "contents": [
              {
                "type": "button",
                "action": {
                  "type": "message",
                  "label": "laplacian_sharpen",
                  "text": "laplacian_sharpen"
                },
                "color": "#1E90FF",
                "gravity": "center"
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "lg",
            "contents": [
              {
                "type": "button",
                "action": {
                  "type": "message",
                  "label": "gaussian_subtract",
                  "text": "gaussian_subtract"
                },
                "color": "#1E90FF",
                "gravity": "center"
              }
            ]
          }
        ]
      }
    ]
  }
}

def flex_output(url, license_plate, province, is_legal=False):
    return {
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": url,
    "size": "full",
    "aspectRatio": "1:1",
    "aspectMode": "cover",
    "action": {
      "type": "uri",
      "label": "Line",
      "uri": url
    }
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "box",
        "layout": "vertical",
        "margin": "sm",
        "contents": [
          {
            "type": "text",
            "text": "ป้ายทะเบียนที่ตรวจพบ",
            "weight": "regular",
            "size": "md",
            "gravity": "center",
            "contents": []
          },
          {
            "type": "text",
            "text": f"{license_plate} {province}" if license_plate != "-1" else "ตรวจไม่พบ",
            "weight": "bold",
            "size": "xl",
            "align": "center",
            "gravity": "center",
            "margin": "md",
            "contents": []
          }
        ]
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "sm",
        "contents": [
          {
            "type": "text",
            "text": "hello, world",
            "align": "start",
            "gravity": "center",
            "margin": "sm",
            "contents": [
              {
                "type": "span",
                "text": "สถานะ : "
              },
              {
                "type": "span",
                "text": "ถูกกฎหมาย" if is_legal else "ไม่มี" if license_plate == "-1" else "ผิดกฎหมาย",
                "color": "#00D61CFF" if is_legal else "#1E90FF" if license_plate == "-1" else "#FC0303",
                "weight": "bold"
              }
            ]
          }
        ]
      }
    ]
  }
}