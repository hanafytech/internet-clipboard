from flask import Flask, request, render_template_string
import base64

app = Flask(__name__)

# SECURITY: Limit uploads to 16MB to protect server RAM and browser limits
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 

db = {}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>internet-clipboard</title>
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
        textarea:focus { outline: none; border-color: #0d6efd; box-shadow: 0 0 0 3px rgba(13, 110, 253, 0.25); }
        button { 
            background-color: #0d6efd; color: white; border: none; padding: 12px 24px; font-size: 16px; 
            font-weight: 600; border-radius: 6px; margin-top: 15px; cursor: pointer; transition: background-color 0.2s; 
        }
        button:hover { background-color: #0b5ed7; }
        .download-btn { 
            display: inline-block; background-color: #198754; color: white; text-decoration: none; 
            padding: 12px 20px; border-radius: 6px; font-weight: 600; margin-top: 10px; transition: 0.2s;
        }
        .download-btn:hover { background-color: #157347; }
        .file-input { 
            display: block; width: 100%; margin-bottom: 5px; padding: 10px; background: #2d2d2d; 
            border: 1px dashed #666; border-radius: 6px; color: #ccc; box-sizing: border-box; cursor: pointer;
        }
        .alert { background-color: #332701; color: #ffda6a; padding: 15px; border-radius: 6px; border-left: 5px solid #ffda6a; margin-bottom: 20px; font-weight: 500; }
        .success { background-color: #0f291a; color: #75b798; padding: 15px; border-radius: 6px; border-left: 5px solid #75b798; margin-bottom: 20px; font-weight: 500; }
        .info-box { background-color: #0c2b4d; color: #9ec5fe; padding: 15px; border-radius: 6px; border-left: 5px solid #9ec5fe; margin-bottom: 20px; font-family: monospace; font-size: 15px; }
        .warning-text { color: #ff6b6b; font-size: 13px; margin-top: 0; margin-bottom: 15px; font-weight: 600; }
        h2 { margin-top: 0; color: #ffffff; border-bottom: 1px solid #333; padding-bottom: 10px; margin-bottom: 20px; font-weight: 500; }
        p { line-height: 1.6; margin-bottom: 10px; }
    </style>
</head>
<body>
    <div class="container">
        {% if status == 'home' %}
            <h2>Welcome to internet-clipboard</h2>
            <p>To create a secure, burn-after-reading paste, simply type a custom name at the end of your URL.</p>
            <div class="info-box">Example: <strong>yourdomain.com/secret123</strong></div>
        {% else %}
            <h2>/{{ path }}</h2>
            
            {% if status == 'saved' %}
                <div class="success">✅ Saved! Share this exact URL. The data will be destroyed the next time it is opened.</div>
                
                {% if paste_data.file_name %}
                    <div class="info-box">📎 Attached: {{ paste_data.file_name }}</div>
                {% endif %}
                {% if paste_data.content %}
                    <textarea readonly>{{ paste_data.content }}</textarea>
                {% endif %}
                
            {% elif status == 'read' %}
                <div class="alert">⚠️ This message has been destroyed. If you refresh this page, it will be gone forever.</div>
                
                {% if paste_data.file_name %}
                    <div class="info-box" style="margin-bottom: 15px;">
                        <p style="margin-top: 0;">📎 Attached File: <strong>{{ paste_data.file_name }}</strong></p>
                        <a href="data:{{ paste_data.file_type }};base64,{{ paste_data.file_data }}" download="{{ paste_data.file_name }}" class="download-btn">Download File</a>
                    </div>
                {% endif %}
                {% if paste_data.content %}
                    <textarea readonly>{{ paste_data.content }}</textarea>
                {% endif %}
                
            {% else %}
                <form method="POST" enctype="multipart/form-data">
                    <input type="file" name="file_upload" class="file-input" />
                    <p class="warning-text">Max file size: 16MB (Stored purely in RAM for maximum security)</p>
                    <textarea name="content" placeholder="Type or paste your text here (optional)..."></textarea>
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
    if not path:
        return render_template_string(HTML_TEMPLATE, path='', paste_data=None, status='home')

    if request.method == 'POST':
        content = request.form.get('content', '')
        file = request.files.get('file_upload')
        
        file_name = None
        file_data = None
        file_type = None

        if file and file.filename:
            file_name = file.filename
            file_type = file.mimetype
            file_data = base64.b64encode(file.read()).decode('utf-8')
            
        if content.strip() or file_name:
            db[path] = {
                'content': content,
                'file_name': file_name,
                'file_type': file_type,
                'file_data': file_data
            }
            return render_template_string(HTML_TEMPLATE, path=path, paste_data=db[path], status='saved')
        
    if path in db:
        paste_data = db.pop(path)
        return render_template_string(HTML_TEMPLATE, path=path, paste_data=paste_data, status='read')
    else:
        return render_template_string(HTML_TEMPLATE, path=path, paste_data=None, status='new')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)