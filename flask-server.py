from flask import Flask, request, send_from_directory
from flask_cors import CORS, cross_origin
import search

app = Flask(__name__)
cors = CORS(app)

@app.route('/<path:path>')
@cross_origin()
def serve_page(path):
    return send_from_directory('pages', path)

@app.route('/process_text')
def process_text():
    chunks = search.split_text(request.args['text'])
    return '\n'.join([str(search.get_results(chunk)) for chunk in chunks])
    
if __name__ == "__main__":
    app.run(port=3000)