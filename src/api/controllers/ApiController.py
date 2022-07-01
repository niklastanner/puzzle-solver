from flask import request, Blueprint

api_controller = Blueprint('api_controller', __name__, template_folder='templates')


@api_controller.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@api_controller.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('/var/www/uploads/uploaded_file.txt')
