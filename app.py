from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# Vulnerable SQL Injection & XSS endpoint
@app.route("/search")
def search():
    query = request.args.get("q", "")
    
    # Vulnerable SQL Query (String Formatting)
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM products WHERE name = '{query}'")
    results = cursor.fetchall()
    
    # Vulnerable Render (Reflected XSS)
    template = f"<h1>Search results for: {query}</h1>"
    return render_template_string(template)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
