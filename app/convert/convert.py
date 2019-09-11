from PIL import Image
from functools import wraps
import time

# ########## CONSTANTS ##########


GREY_SCALE_SYMBOLS = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{}[]?-_+~i!lI;:,\"^`"
LENGTH = len(GREY_SCALE_SYMBOLS)
GREY_SCALE = "L"
FILE_FORMATS = ['jpeg', 'jpg']

# ########## STATUS CODES ##########


CODES = [IMAGE_NOT_FOUND, INVALID_IMAGE_FORMAT, IMAGE_ERROR, TEXT_FILE_ERROR, INVALID_WIDTH] = range(-1, -6, -1)


# ########## METHODS ##########


def handle_io_error(f):
    """ Handle exceptions """

    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            print(f"{time.strftime('%Y-%m-%d %H:%M:%S')}: "
                  f"Catch Exception {type(e).__name__} when "
                  f"calling {f.__name__} with args [{list(args) + list(kwargs.items())}]")
            return None

    return wrapper


@handle_io_error
def load(fp):
    """ Load an image via file path """
    return Image.open(fp)


@handle_io_error
def save(fp, text):
    with open(fp, "w") as f:
        f.write(text)
    return True


def resize(img, new_width=120) -> Image:
    """ Resize an image while preserving it's aspect ratio """
    return img.resize(resize_dim(img, new_width))


def resize_dim(img, new_width):
    """ Calculate new dimensions while preserving the image's aspect ratio """
    old_width, old_height = img.size
    aspect_ratio = float(old_height) / float(old_width)
    new_height = int(aspect_ratio * new_width)
    return new_width, new_height


def to_grayscale(img) -> Image:
    """ Convert an image to grayscale """
    return img.convert(GREY_SCALE)


def to_ascii(pixel) -> str:
    """ Convert a grayscale pixel into it's ASCII equivalent """
    return GREY_SCALE_SYMBOLS[pixel // LENGTH]


def convert(img: Image):
    """ Convert an image to ASCII """
    for pixel in list(img.getdata()):
        yield to_ascii(pixel)


def convert_img_to_ascii(fp_in, fp_out, new_width=100):
    """
    Convert a image to ascii.
    :param fp_in: Filepath to image
    :param fp_out: Fileout path
    :param new_width: Output width
    :return: Negative integer status code if fail, else 0
    """
    if fp_in.split('.')[-1] not in FILE_FORMATS:
        return INVALID_IMAGE_FORMAT

    img = load(fp_in)
    if not img:
        return IMAGE_NOT_FOUND

    gray_img = to_grayscale(resize(img, new_width))

    s = ""
    for i, pixel in enumerate(convert(gray_img)):
        if i % new_width == 0:
            s += "\n"
        else:
            s += pixel

    if not save(fp_out, s):
        return TEXT_FILE_ERROR

    return 0
