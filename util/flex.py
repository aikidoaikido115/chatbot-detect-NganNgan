def flex_select_enhance():
    return {
  "type": "bubble",
  "direction": "ltr",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "เลือกวิธี enhance รูป",
        "align": "center",
        "contents": []
      },
      {
        "type": "button",
        "action": {
          "type": "message",
          "label": "conv_sharpen",
          "text": "conv_sharpen"
        }
      },
      {
        "type": "button",
        "action": {
          "type": "message",
          "label": "unsharp_mask",
          "text": "unsharp_mask"
        }
      },
      {
        "type": "button",
        "action": {
          "type": "message",
          "label": "laplacian_sharpen",
          "text": "laplacian_sharpen"
        }
      },
      {
        "type": "button",
        "action": {
          "type": "message",
          "label": "gaussian_subtract",
          "text": "gaussian_subtract"
        }
      }
    ]
  }
}

def flex_output(url, license_plate, province):
    return {
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": url,
    "size": "full",
    "aspectRatio": "20:13",
    "aspectMode": "cover",
    "action": {
      "type": "uri",
      "label": "Action",
      "uri": url
    }
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "spacing": "md",
    "action": {
      "type": "uri",
      "label": "Action",
      "uri": "https://linecorp.com"
    },
    "contents": [
      {
        "type": "text",
        "text": "ข้อมูลที่ตรวจพบ",
        "weight": "bold",
        "size": "xl",
        "contents": []
      },
      {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
          {
            "type": "box",
            "layout": "baseline",
            "contents": [
              {
                "type": "text",
                "text": "ทะเบียน",
                "weight": "bold",
                "margin": "sm",
                "contents": []
              },
              {
                "type": "text",
                "text": license_plate,
                "size": "sm",
                "color": "#AAAAAA",
                "align": "end",
                "contents": []
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "contents": [
              {
                "type": "text",
                "text": "จังหวัด",
                "weight": "bold",
                "flex": 0,
                "margin": "sm",
                "contents": []
              },
              {
                "type": "text",
                "text": province,
                "size": "sm",
                "color": "#AAAAAA",
                "align": "end",
                "contents": []
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "contents": [
              {
                "type": "text",
                "text": "สถานะ",
                "weight": "bold",
                "flex": 0,
                "margin": "sm",
                "contents": []
              },
              {
                "type": "text",
                "text": "ผิดกฎจราจร",
                "size": "sm",
                "color": "#FF0000FF",
                "align": "end",
                "contents": []
              }
            ]
          }
        ]
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "spacer",
        "size": "xxl"
      },
      {
        "type": "button",
        "action": {
          "type": "message",
          "label": "ไปที่เมนู",
          "text": "menu_select"
        },
        "color": "#448190FF",
        "style": "primary"
      }
    ]
  }
}