from flask import Flask, request, render_template_string
import os

app = Flask(__name__)
db = {}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Secure Paste</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; background-color: #f9f9f9; color: #333; }
        .container { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        textarea { width: 100%; height: 300px; font-family: monospace; padding: 10px; border: 1px solid #ccc; border-radius: 4px; resize: vertical; box-sizing: border-box; }
        button { background-color: #007bff; color: white; border: none; padding: 10px 20px; font-size: 16px; border-radius: 4px; margin-top: 15px; cursor: pointer; transition: background 0.2s; }
        button:hover { background-color: #0056b3; }
        .alert { background-color: #fff3cd; color: #856404; padding: 15px; border-radius: 4px; border-left: 4px solid #ffeeba; margin-bottom: 20px; font-weight: bold; }
        .success { background-color: #d4edda; color: #155724; padding: 15px; border-radius: 4px; border-left: 4px solid #c3e6cb; margin-bottom: 20px; font-weight: bold; }
        h2 { margin-top: 0; color: #222; }
    </style>
</head>
<body>
    <div class="container">
        <h2>/{{ path }}</h2>
        {% if status == 'saved' %}
            <div class="success">✅ Saved! Share this exact URL. The data will be destroyed the next time it is opened.</div>
            <textarea readonly>{{ content }}</textarea>
        {% elif content is not none %}
            <div class="alert">⚠️ This message has been destroyed. If you refresh this page, it will be gone forever.</div>
            <textarea readonly>{{ content }}</textarea>
        {% else %}
            <form method="POST">
                <textarea name="content" placeholder="Type or paste your text here..."></textarea>
                <button type="submit">Save (Burn on Next Read)</button>
            </form>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
    if not path:
        return "Welcome to the Pastebin. Add a custom name to the end of the URL to create a paste. Example: yourdomain.com/secret123"

    if request.method == 'POST':
        content = request.form.get('content', '')
        if content.strip():
            db[path] = content
            return render_template_string(HTML_TEMPLATE, path=path, content=content, status='saved')
        
    if path in db:
        content = db.pop(path)
        return render_template_string(HTML_TEMPLATE, path=path, content=content, status='read')
    else:
        return render_template_string(HTML_TEMPLATE, path=path, content=None, status='new')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)