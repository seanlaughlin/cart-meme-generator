from flask import Flask, request, render_template, send_file, send_from_directory
from PIL import Image
import os
from rembg import remove

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
BACKGROUND_FOLDER = 'static/backgrounds'
CART_BACK_PATH = 'static/Cart_Main.png'
CART_FRONT_PATH = 'static/Cart_Front.png'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

def resize_image_maintain_aspect_ratio(image, height):
    # Calculate the width using the aspect ratio
    width = int((height / float(image.size[1])) * image.size[0])
    return image.resize((width, height), Image.Resampling.LANCZOS)

def crop_to_content(image):
    bbox = image.getbbox()
    if bbox:
        return image.crop(bbox)
    return image

def create_meme(uploaded_image_path, background_image_path, cart_back_path, cart_front_path, output_path):
    # Open the images
    cart_back = Image.open(cart_back_path).convert("RGBA")
    cart_front = Image.open(cart_front_path).convert("RGBA")

    # Create a new image with the same size as the cart
    meme = Image.new("RGBA", cart_back.size)

    # Optionally add the background image if it is not 'bg_0.png'
    print(background_image_path)
    print(background_image_path != 'static/backgrounds\\bg_0.png')
    if background_image_path != 'static/backgrounds\\bg_0.png':
        background_image = Image.open(background_image_path).convert("RGBA")
        background_image = background_image.resize(cart_back.size, Image.Resampling.LANCZOS)
        meme.paste(background_image, (0, 0))

    meme.paste(cart_back, (0, 0), mask=cart_back)
    if uploaded_image_path:
        uploaded_image = Image.open(uploaded_image_path).convert("RGBA")
        uploaded_image = remove(uploaded_image)
        uploaded_image = crop_to_content(uploaded_image)
        uploaded_image = resize_image_maintain_aspect_ratio(uploaded_image, 1000)

        cart_width, cart_height = cart_back.size
        x_offset = ((cart_width - uploaded_image.width) // 2) + 100
        y_offset = cart_height - 1850  # Adjust y_offset if needed

        meme.paste(uploaded_image, (x_offset, y_offset), mask=uploaded_image)
    meme.paste(cart_front, (0, 0), mask=cart_front)

    meme.save(output_path, format="PNG")

@app.route('/')
def upload_form():
    backgrounds = [f for f in os.listdir(BACKGROUND_FOLDER) if os.path.isfile(os.path.join(BACKGROUND_FOLDER, f))]
    return render_template('upload.html', backgrounds=backgrounds)

@app.route('/upload', methods=['POST'])
def upload_image():
    file = request.files.get('file')
    background_filename = request.form.get('background')
    if not background_filename:
        return "No background selected"

    background_path = os.path.join(BACKGROUND_FOLDER, background_filename)
    if not os.path.isfile(background_path):
        return "Selected background file does not exist"

    file_path = None
    if file and file.filename != '':
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

    output_path = os.path.join(OUTPUT_FOLDER, 'output_meme.png')
    create_meme(file_path, background_path, CART_BACK_PATH, CART_FRONT_PATH, output_path)
    return send_from_directory(OUTPUT_FOLDER, 'output_meme.png')

@app.route('/outputs/<filename>')
def uploaded_file(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True)
