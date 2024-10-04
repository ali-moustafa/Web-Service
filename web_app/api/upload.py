from flask import Blueprint, request, jsonify, abort, current_app
from werkzeug.utils import secure_filename
import os

upload_blueprint = Blueprint('upload_blueprint', __name__)


@upload_blueprint.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        abort(400, 'No file uploaded!')

    file = request.files['file']
    if file.filename == '':
        abort(400, 'Please provide filename!')

    filename = secure_filename(file.filename)
    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
    return jsonify(message=f"File '{filename}' uploaded successfully"), 200
