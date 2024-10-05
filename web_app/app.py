from flask import Flask
from flask_smorest import Api
import os

from web_app.api.upload import upload_blueprint
from web_app.api.file import file_blueprint


def create_app():
    app = Flask(__name__)

    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploaded_files')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024    # configure file size

    app.config['API_TITLE'] = 'Web Service API'
    app.config['API_VERSION'] = 'v1'
    app.config['OPENAPI_VERSION'] = '3.0.2'
    app.config['OPENAPI_URL_PREFIX'] = '/docs'
    app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger-ui'
    app.config['OPENAPI_SWAGGER_UI_URL'] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'

    api = Api(app)

    api_url = '/'
    api.register_blueprint(upload_blueprint, name="upload_file", url_prefix=api_url)
    api.register_blueprint(file_blueprint, name="process_file", url_prefix=api_url)

    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    @app.route('/docs')
    def swagger_ui():
        return '''
        <html>
          <head>
            <link href="https://cdn.jsdelivr.net/npm/swagger-ui-dist/swagger-ui.css" rel="stylesheet" />
          </head>
          <body>
            <div id="swagger-ui"></div>
            <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist/swagger-ui-bundle.js"></script>
            <script>
              const ui = SwaggerUIBundle({
                url: '/docs/openapi.json',
                dom_id: '#swagger-ui',
              })
            </script>
          </body>
        </html>
        '''

    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    create_app()
