from flask import jsonify, current_app
from werkzeug.utils import secure_filename
from flask_smorest import Blueprint, abort
from marshmallow import Schema, fields
import os


upload_blueprint = Blueprint('upload_blueprint', __name__)


class FileUploadSchema(Schema):
    file = fields.Raw(type='file', required=True)


@upload_blueprint.route('/upload', methods=['POST'])
@upload_blueprint.arguments(FileUploadSchema, location='files')
def upload_file(arg):
    """
    Upload a txt file
    """
    file = arg['file']
    if file.filename == '':
        abort(400, message='Please provide filename!')

    filename = secure_filename(file.filename)
    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
    return jsonify(message=f"File '{filename}' uploaded successfully"), 200
