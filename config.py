import os


class Config:
    UPLOAD_FOLDER = 'uploads'
    OUTPUT_FOLDER = 'outputs'
    BACKGROUND_FOLDER = 'static/backgrounds'
    CART_BACK_PATH = 'static/Cart_Main.png'
    CART_FRONT_PATH = 'static/Cart_Front.png'
    DEFAULT_BACKGROUND_PATH = os.path.join(BACKGROUND_FOLDER, 'bg_0.jpg')
    DEBUG = False
    TESTING = False
