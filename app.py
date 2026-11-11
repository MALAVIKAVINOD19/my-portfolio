
from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)


# Create the database

def init_db():
    connection = sqlite3.connect("portfolio.db")

    connection.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


init_db()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/contact", methods=["POST"])
def contact():

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    message = request.form.get("message", "").strip()


    # Validate the form

    if not name or not email or not message:
        return """
        <h2>All fields are required!</h2>
        <a href="/">Go Back</a>
        """, 400


    if "@" not in email or "." not in email.split("@")[-1]:
        return """
        <h2>Please enter a valid email address!</h2>
        <a href="/">Go Back</a>
        """, 400


    # Save message in database

    connection = sqlite3.connect("portfolio.db")

    connection.execute(
        "INSERT INTO messages (name, email, message) VALUES (?, ?, ?)",
        (name, email, message)
    )

    connection.commit()
    connection.close()


    print("New Contact Message!")
    print("Name:", name)
    print("Email:", email)
    print("Message:", message)

    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

