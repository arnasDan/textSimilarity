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
    search_string = request.args['text']
    if not search_string.strip():
        return 'No text!'
    else:
        chunks = search.split_text(search_string)
        try:
            return '\n'.join([str(search.get_results(chunk)) for chunk in chunks])
        except Exception as e:
            return 'An error occured: %s \n Please try again later' % repr(e)

if __name__ == "__main__":
    app.run(port=3000, debug=True)