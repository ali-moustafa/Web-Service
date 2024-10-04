from flask import Flask
import os

from web_app.api.upload import upload_blueprint
from web_app.api.file import file_blueprint


def create_app():
    app = Flask(__name__)

    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploaded_files')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024    # configure file size

    api_url = '/'

    app.register_blueprint(upload_blueprint, name="upload_file", url_prefix=api_url)
    app.register_blueprint(file_blueprint, name="process_file", url_prefix=api_url)

    app.run(debug=True)


if __name__ == '__main__':
    create_app()
