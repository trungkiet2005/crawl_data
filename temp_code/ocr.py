import cv2
import pytesseract

img = cv2.imread("page_1.png", cv2.IMREAD_GRAYSCALE)
# Threshold thành ảnh đen trắng
_, img = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)
# Resize để chữ nhỏ rõ hơn
img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

captcha_text = pytesseract.image_to_string(
    img,
    config="--psm 3 -l vie"
)
print(captcha_text)
