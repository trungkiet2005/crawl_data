import pytesseract
from pdf2image import convert_from_path
from PIL import Image

pdf_path = "./dataset/143_Ban_an_phat_hanh_Nguyen_Thi_Dong__Giet_nguoi_ngay_0242024.pdf"

images = convert_from_path(pdf_path)

for i, image in enumerate(images):
    
    # image_path = f"page_{i+1}.png"
    # image.save(image_path, "PNG")
    
    text = pytesseract.image_to_string(
        image,
        config="--psm 3 -l vie"
    )
    print(f"--- Text from page {i+1} ---")
    print(text)
    print("\n")