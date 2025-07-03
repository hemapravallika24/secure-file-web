from flask import Flask, render_template, request, send_file
from cryptography.fernet import Fernet
import os

app = Flask(__name__)
key = Fernet.generate_key()  # For demo; in production, save/load securely!
f = Fernet(key)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/encrypt", methods=["POST"])
def encrypt():
    file = request.files["file"]
    data = file.read()
    encrypted = f.encrypt(data)
    enc_filename = "encrypted_" + file.filename
    with open(enc_filename, "wb") as f_out:
        f_out.write(encrypted)
    return send_file(enc_filename, as_attachment=True)

@app.route("/decrypt", methods=["POST"])
def decrypt():
    file = request.files["file"]
    data = file.read()
    decrypted = f.decrypt(data)
    dec_filename = "decrypted_" + file.filename.replace("encrypted_", "")
    with open(dec_filename, "wb") as f_out:
        f_out.write(decrypted)
    return send_file(dec_filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
