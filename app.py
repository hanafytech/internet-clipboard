from flask import Flask, request, render_template_string

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
        body { 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; 
            max-width: 800px; 
            margin: 40px auto; 
            padding: 20px; 
            background-color: #121212; 
            color: #e0e0e0; 
        }
        .container { 
            background: #1e1e1e; 
            padding: 30px; 
            border-radius: 10px; 
            box-shadow: 0 8px 16px rgba(0,0,0,0.6); 
        }
        textarea { 
            width: 100%; 
            height: 300px; 
            font-family: 'Courier New', Courier, monospace; 
            padding: 15px; 
            background-color: #2d2d2d; 
            color: #f8f8f2; 
            border: 1px solid #444; 
            border-radius: 6px; 
            resize: vertical; 
            box-sizing: border-box; 
            font-size: 15px;
            line-height: 1.5;
        }
        textarea:focus {
            outline: none;
            border-color: #0d6efd;
            box-shadow: 0 0 0 3px rgba(13, 110, 253, 0.25);
        }
        button { 
            background-color: #0d6efd; 
            color: white; 
            border: none; 
            padding: 12px 24px; 
            font-size: 16px; 
            font-weight: 600;
            border-radius: 6px; 
            margin-top: 15px; 
            cursor: pointer; 
            transition: background-color 0.2s ease-in-out; 
        }
        button:hover { 
            background-color: #0b5ed7; 
        }
        .alert { 
            background-color: #332701; 
            color: #ffda6a; 
            padding: 15px; 
            border-radius: 6px; 
            border-left: 5px solid #ffda6a; 
            margin-bottom: 20px; 
            font-weight: 500; 
        }
        .success { 
            background-color: #0f291a; 
            color: #75b798; 
            padding: 15px; 
            border-radius: 6px; 
            border-left: 5px solid #75b798; 
            margin-bottom: 20px; 
            font-weight: 500; 
        }
        .info-box {
            background-color: #0c2b4d;
            color: #9ec5fe;
            padding: 15px;
            border-radius: 6px;
            border-left: 5px solid #9ec5fe;
            margin-top: 20px;
            font-family: 'Courier New', Courier, monospace;
            font-size: 15px;
        }
        h2 { 
            margin-top: 0; 
            color: #ffffff; 
            border-bottom: 1px solid #333;
            padding-bottom: 10px;
            margin-bottom: 20px;
            font-weight: 500;
            letter-spacing: 0.5px;
        }
        p {
            font-size: 16px;
            line-height: 1.6;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        {% if status == 'home' %}
            <h2>Welcome to Secure Paste</h2>
            <p>To create a secure, burn-after-reading paste, simply type a custom name at the end of your URL.</p>
            <div class="info-box">
                Example: <strong>yourdomain.com/secret123</strong>
            </div>
        {% else %}
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
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
    # Route for the root domain
    if not path:
        return render_template_string(HTML_TEMPLATE, path='', content=None, status='home')

    # Route for saving a new paste
    if request.method == 'POST':
        content = request.form.get('content', '')
        if content.strip():
            db[path] = content
            return render_template_string(HTML_TEMPLATE, path=path, content=content, status='saved')
        
    # Route for reading an existing paste
    if path in db:
        content = db.pop(path)
        return render_template_string(HTML_TEMPLATE, path=path, content=content, status='read')
    else:
        return render_template_string(HTML_TEMPLATE, path=path, content=None, status='new')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)