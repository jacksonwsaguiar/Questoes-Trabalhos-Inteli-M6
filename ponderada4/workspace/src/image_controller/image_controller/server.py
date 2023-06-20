from flask import Flask, render_template, request, send_from_directory, Response
import sqlite3
import time

UPLOAD_FOLDER = '/home/jacksonaguiar/Questoes-Trabalhos-Inteli-M6/ponderada4/workspace/src/image_controller/image_controller/static/images'

app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    conn = get_db_connection()
    images = conn.execute('SELECT * FROM images').fetchall()
    conn.close()
    return render_template('index.html', images=images)


@app.route("/upload", methods=["POST"])
def upload():
    conn = get_db_connection()
    filename = f"img-{time.time()}.jpg"
    storage = UPLOAD_FOLDER + "/"+filename

    with open(storage, 'wb') as f:
        f.write(request.data)
        f.close()

    conn.execute('INSERT INTO images (image_name) VALUES (?)', (filename,))
    conn.commit()
    conn.close()

    return 'file uploaded successfully'


if __name__ == '__main__':
    app.run(debug=True, port=8080)
