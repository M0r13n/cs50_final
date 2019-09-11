import os
from hashlib import sha1
from flask import Flask, render_template, redirect, url_for, send_from_directory, Response, abort
from .forms import UploadForm
from .config import BaseConfig
from .convert import *
from functools import wraps

app = Flask(__name__)
app.config.from_object(BaseConfig)


def handle_io_exception(f):
    @wraps(f)
    def handle(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            app.logger.error(f"Could save file, because the following error occured {type(e).__name__}: {str(e)}")
            return None

    return handle


@handle_io_exception
def save_file(f):
    # use hash to prevent collisions
    sha1_hash = sha1(f.filename.encode("utf-8")).hexdigest()
    path = store_path(sha1_hash)
    f.save(path)
    return sha1_hash, path


def store_path(sha1_hash):
    return os.path.join(app.root_path, app.config["DATA_DIR"], in_name(sha1_hash))


def download_path(sha1_hash):
    return os.path.join(app.root_path, app.config["OUT_DIR"], out_name(sha1_hash))


def in_name(sha1_hash):
    return f"in_{sha1_hash}.jpg"


def out_name(sha1_hash):
    return f"out_{sha1_hash}.txt"


@app.route('/', methods=["GET", "POST"])
def index():
    upload = UploadForm()
    if upload.validate_on_submit():
        # Save image
        success = save_file(upload.file.data)
        if not success:
            abort(500)
        sha1_hash, path = success
        # Convert Image
        status_code = convert_img_to_ascii(path, download_path(sha1_hash), new_width=250)
        if status_code < 0:
            app.logger.error(f"Converter exited with STATUS_CODE: {status_code}")
            abort(500)
        return redirect(url_for(".result", sha1_hash=sha1_hash))
    return render_template("index.html", upload=upload)


@app.route('/result?<string:sha1_hash>', methods=["GET"])
def result(sha1_hash):
    return render_template("result.html", sha1_hash=sha1_hash)


@app.route('/uploads/<string:sha1_hash>', methods=['GET'])
def download(sha1_hash):
    d = os.path.join(app.root_path, app.config['OUT_DIR'])
    return send_from_directory(directory=d, filename=out_name(sha1_hash))


@app.route('/500', methods=['GET'])
def five_hundred():
    return render_template("500.html"), 500


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error_page(error):
    return render_template("500.html"), 500


if __name__ == '__main__':
    app.run()
