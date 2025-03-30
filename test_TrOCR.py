from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image, ImageOps


processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")


image_path = "test.png"
image = Image.open(image_path).convert("RGB")


# image = ImageOps.grayscale(image)
image = ImageOps.autocontrast(image)
image = image.resize((300, 100))


pixel_values = processor(images=image, return_tensors="pt").pixel_values
generated_ids = model.generate(pixel_values)
ocr_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

print(ocr_text)