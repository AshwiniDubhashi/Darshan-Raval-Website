from flask import Flask, render_template, request, redirect
import mysql.connector
import os

app = Flask(__name__)

UPLOAD_FOLDER = "static/songs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="darshansongs"
)

@app.route("/")
def songs():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM songs")
    songs = cursor.fetchall()
    return render_template("songs.html", songs=songs)

@app.route("/uploads", methods=["GET","POST"])
def uploads():
    if request.method == "POST":
        print("Upload button clicked")

        title = request.form["title"]
        file = request.files["file"]

        print("Title:", title)
        print("File:", file.filename)

        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO songs (title, filename) VALUES (%s,%s)",
            (title, file.filename)
        )
        db.commit()

        print("Saved to database")

        return redirect("/")

    return render_template("uploads.html")
if __name__ == "__main__":
    app.run(debug=True)