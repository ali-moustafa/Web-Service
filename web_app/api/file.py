from flask import request, Response, jsonify, current_app
from flask_smorest import Blueprint, abort
from marshmallow import Schema, fields
import os
import random
import xml.etree.ElementTree as ET


file_blueprint = Blueprint('file_blueprint', __name__)


class FileNameSchema(Schema):
    file_name = fields.String(required=True)


def file_random_line(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        random_line = random.choice(lines).strip()
        return random_line


@file_blueprint.route('/random_line', methods=['GET'])
def get_random_line():
    """
    Return one random line of a random previously uploaded file
    """
    upload_directory = current_app.config['UPLOAD_FOLDER']
    files = os.listdir(upload_directory)
    if not files:
        abort(404, message='No files uploaded yet!')

    file_name = random.choice(files)
    file_path = os.path.join(upload_directory, file_name)
    if not os.path.isfile(file_path):
        abort(404, message=f"file {file_name} does not exist!")

    random_line = file_random_line(file_path)
    most_common_letter = max(set(random_line), key=random_line.count)

    if 'application/json' in request.accept_mimetypes:
        return jsonify({
            'file_name': file_name,
            'line': random_line,
            'most_common_letter': most_common_letter
        })
    elif 'application/xml' in request.accept_mimetypes:
        root = ET.Element('random_line')
        ET.SubElement(root, 'file_name').text = file_name
        ET.SubElement(root, 'line').text = random_line
        ET.SubElement(root, 'most_common_letter').text = most_common_letter
        return Response(ET.tostring(root), mimetype='application/xml')
    else:
        return random_line


@file_blueprint.route('/random_line_backwards', methods=['GET'])
@file_blueprint.arguments(FileNameSchema, location='query')
def get_random_line_backwards(arg):
    """
    Return one random line backwards
    """
    upload_directory = current_app.config['UPLOAD_FOLDER']
    files = os.listdir(upload_directory)
    if not files:
        abort(404, message='No uploaded files found!')

    file_name = arg['file_name']
    if file_name not in files:
        abort(404, message=f"File '{file_name}' not found")

    file_path = os.path.join(upload_directory, file_name)
    random_line = file_random_line(file_path)
    random_line_backwards = random_line[::-1]

    return jsonify({'random_line_backwards': random_line_backwards}), 200


@file_blueprint.route('/hundred_longest_lines')
def hundred_longest_lines_in_all_files():
    """
    Return the 100 longest lines of all files uploaded
    """
    upload_directory = current_app.config['UPLOAD_FOLDER']
    files = os.listdir(upload_directory)
    all_lines = []
    num_lines = 100
    for file_name in files:
        file_path = os.path.join(upload_directory, file_name)
        with open(file_path, 'r') as file:
            lines = file.readlines()
            all_lines.extend(lines)

    longest_lines = sorted(all_lines, key=len, reverse=True)[:num_lines]
    return jsonify({'100_longest_lines': longest_lines})


@file_blueprint.route('/twenty_longest_lines')
@file_blueprint.arguments(FileNameSchema, location='query')
def get_twenty_longest_lines_one_file(arg):
    """
    Return the 20 longest lines of an uploaded file
    """
    upload_directory = current_app.config['UPLOAD_FOLDER']
    files = os.listdir(upload_directory)

    if not files:
        abort(404, message='No uploaded files found!')

    file_name = arg['file_name']
    if file_name not in files:
        abort(404, message=f"File '{file_name}' not found")

    with open(os.path.join(upload_directory, file_name), 'r') as file:
        lines = file.readlines()
        longest_lines = sorted(lines, key=len, reverse=True)[:20]

    return jsonify({'file_name': file_name, '20_longest_lines': longest_lines}), 200
