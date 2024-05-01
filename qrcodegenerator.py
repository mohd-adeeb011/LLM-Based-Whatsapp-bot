import qrcode
from PIL import Image

# Your WhatsApp number
whatsapp_number = "+14155238886"

# Generate QR code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)
qr.add_data(f"https://wa.me/{whatsapp_number}")
qr.make(fit=True)

# Create an image from the QR code instance
img = qr.make_image(fill_color="black", back_color="white")

# Save the image
img.save("whatsapp_qr1.png")
