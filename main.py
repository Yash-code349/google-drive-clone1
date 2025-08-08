from flask import Flask, render_template, request, jsonify
from s3_utils import upload_to_s3, delete_from_s3
import sqlite3

app = Flask(__name__)
DB_PATH = "db.sqlite3"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            s3_url TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_file_metadata(filename, s3_url):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO files (filename, s3_url) VALUES (?, ?)", (filename, s3_url))
    conn.commit()
    conn.close()

def get_all_files():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, filename, s3_url FROM files")
    files = cursor.fetchall()
    conn.close()
    return [{"id": f[0], "filename": f[1], "url": f[2]} for f in files]

@app.route('/')
def index():
    files = get_all_files()
    return render_template("index.html", files=files)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if file:
        s3_url = upload_to_s3(file)
        save_file_metadata(file.filename, s3_url)
        return jsonify({"message": "File uploaded", "url": s3_url})
    return jsonify({"error": "No file uploaded"}), 400

@app.route('/upload', methods=['GET'])
def show_uploaded_files():
    files = get_all_files()
    return render_template("files.html", files=files)

@app.route('/delete/<int:file_id>', methods=['DELETE'])
def delete(file_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT filename FROM files WHERE id=?", (file_id,))
    row = c.fetchone()
    if row:
        filename = row[0]
        delete_from_s3(filename)
        c.execute("DELETE FROM files WHERE id=?", (file_id,))
        conn.commit()
        conn.close()
        return jsonify({"message": "File deleted"})
    conn.close()
    return jsonify({"error": "File not found"}), 404

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)
