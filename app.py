# Creating a basic starter template for SatoLink using Flask (Python web framework)
# This app allows users to register a short username and associate it with a Bitcoin Cash (BCH) address.
# Visiting satolink/username will show their QR code and BCH address for tips.

import qrcode
from flask import Flask, request, redirect, render_template_string, url_for
import os

app = Flask(__name__)

# In-memory database to store username → BCH address mappings
# In production, this would be a real database (SQLite, Firebase, etc.)
users = {}

# HTML template for the user's tip page
TEMPLATE = """
<!doctype html>
<html lang="en">
  <head>
    <title>{{ username }} | SatoLink</title>
    <style>
      body { font-family: Arial; text-align: center; padding: 40px; }
      .qr { margin-top: 20px; }
      input.copy-input { width: 80%; padding: 10px; margin-top: 10px; font-size: 1em; }
      button.copy-btn { margin-top: 10px; padding: 10px 20px; font-size: 1em; }
    </style>
  </head>
  <body>
    <h1>@{{ username }}</h1>
    <p>Send Bitcoin Cash (BCH) tips to this address:</p>
    <img src="{{ url_for('static', filename=qr_path) }}" class="qr" width="200">
    <input class="copy-input" value="{{ bch_address }}" id="bchAddress" readonly>
    <br>
    <button onclick="copyText()" class="copy-btn">Copy Address</button>
    <script>
      function copyText() {
        var copyText = document.getElementById("bchAddress");
        copyText.select();
        document.execCommand("copy");
        alert("BCH Address copied!");
      }
    </script>
  </body>
</html>
"""

# Route to register a new shortlink
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form.get("username").strip().lower()
        bch_address = request.form.get("bch_address").strip()
        if not username or not bch_address:
            return "Both fields required", 400
        if username in users:
            return "Username already taken!", 409

        # Save user mapping
        users[username] = bch_address

        # Generate QR code and save to static folder
        img = qrcode.make(bch_address)
        qr_path = f"{username}.png"
        img.save(f"static/{qr_path}")

        return redirect(url_for("tip_page", username=username))

    return """
    <h2>Register Your SatoLink</h2>
    <form method="POST">
      Username: <input name="username" required><br><br>
      BCH Address: <input name="bch_address" required><br><br>
      <button type="submit">Create My Link</button>
    </form>
    """

# Route for tip page
@app.route("/<username>")
def tip_page(username):
    username = username.lower()
    bch_address = users.get(username)
    if not bch_address:
        return "User not found", 404
    qr_path = f"{username}.png"
    return render_template_string(TEMPLATE, username=username, bch_address=bch_address, qr_path=qr_path)

# Create static folder if not exists
os.makedirs("static", exist_ok=True)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
# Your Flask app code will go here (from the previous template)