from flask import Flask, request, render_template, send_from_directory
from PIL import Image
import os
from rembg import remove
import logging

app = Flask(__name__)
app.config.from_object('config.Config')

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
if not os.path.exists(app.config['OUTPUT_FOLDER']):
    os.makedirs(app.config['OUTPUT_FOLDER'])


def resize_image_maintain_aspect_ratio(image, height):
    width = int((height / float(image.size[1])) * image.size[0])
    return image.resize((width, height), Image.Resampling.LANCZOS)


def crop_to_content(image):
    bbox = image.getbbox()
    if bbox:
        return image.crop(bbox)
    return image


def create_meme(uploaded_image_path, background_image_path, cart_back_path, cart_front_path, output_path):
    cart_back = Image.open(cart_back_path).convert("RGBA")
    cart_front = Image.open(cart_front_path).convert("RGBA")
    meme = Image.new("RGBA", cart_back.size)

    if background_image_path != app.config['DEFAULT_BACKGROUND_PATH']:
        background_image = Image.open(background_image_path).convert("RGBA")
        background_image = background_image.resize(cart_back.size, Image.Resampling.LANCZOS)
        meme.paste(background_image, (0, 0))

    meme.paste(cart_back, (0, 0), mask=cart_back)
    if uploaded_image_path:
        uploaded_image = Image.open(uploaded_image_path).convert("RGBA")
        uploaded_image = remove(uploaded_image)
        uploaded_image = crop_to_content(uploaded_image)
        uploaded_image = resize_image_maintain_aspect_ratio(uploaded_image, 500)

        cart_width, cart_height = cart_back.size
        x_offset = ((cart_width - uploaded_image.width) // 2) + 50
        y_offset = cart_height - 925  # Adjust y_offset if needed

        meme.paste(uploaded_image, (x_offset, y_offset), mask=uploaded_image)
    meme.paste(cart_front, (0, 0), mask=cart_front)

    meme.save(output_path, format="PNG")


@app.route('/')
def upload_form():
    backgrounds = []
    for f in os.listdir(app.config['BACKGROUND_FOLDER']):
        if f.startswith('bg_') and f.endswith('.jpg') and not f.startswith('bg_thumb_'):
            num = f.split('_')[-1].split('.')[0]
            thumb_filename = f"bg_thumb_{num}.jpg"
            backgrounds.append((thumb_filename, f))
    return render_template('index.html', backgrounds=backgrounds)


@app.route('/mob')
def upload_form_mob():
    backgrounds = []
    for f in os.listdir(app.config['BACKGROUND_FOLDER']):
        if f.startswith('bg_') and f.endswith('.jpg') and not f.startswith('bg_thumb_'):
            num = f.split('_')[-1].split('.')[0]
            thumb_filename = f"bg_thumb_{num}.jpg"
            backgrounds.append((thumb_filename, f))
    return render_template('index_mob.html', backgrounds=backgrounds)


@app.route('/upload', methods=['POST'])
def upload_image():
    file = request.files.get('file')
    background_filename = request.form.get('background')
    if not background_filename:
        return "No background selected", 400

    background_path = os.path.join(app.config['BACKGROUND_FOLDER'], background_filename)
    if not os.path.isfile(background_path):
        return "Selected background file does not exist", 400

    file_path = None
    if file and file.filename != '':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

    output_path = os.path.join(app.config['OUTPUT_FOLDER'], 'output_meme.png')
    create_meme(file_path, background_path, app.config['CART_BACK_PATH'], app.config['CART_FRONT_PATH'], output_path)
    return send_from_directory(app.config['OUTPUT_FOLDER'], 'output_meme.png')


@app.route('/outputs/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
