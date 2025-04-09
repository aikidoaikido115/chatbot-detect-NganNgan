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