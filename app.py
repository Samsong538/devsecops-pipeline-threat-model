from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route("/search")
def search():
    query = request.args.get("q", "")
    
    # Intentionally vulnerable to Reflected XSS for DAST detection
    template = f"<h1>Search results for: {query}</h1>"
    return render_template_string(template)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
