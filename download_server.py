
from flask import Flask, send_file, render_template_string
import os
import create_zip
import threading
import webbrowser
from pathlib import Path

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>AiogramShopBot Project Download</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            max-width: 800px; 
            margin: 50px auto; 
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
        }
        .download-btn {
            background-color: #4CAF50;
            color: white;
            padding: 15px 30px;
            text-decoration: none;
            border-radius: 5px;
            font-size: 18px;
            display: inline-block;
            margin-top: 20px;
        }
        .download-btn:hover {
            background-color: #45a049;
        }
        .info {
            margin: 20px 0;
            padding: 15px;
            background-color: #e8f4fd;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 AiogramShopBot Project</h1>
        <div class="info">
            <p><strong>📁 Dosya:</strong> {{ filename }}</p>
            <p><strong>📊 Boyut:</strong> {{ size_mb }} MB</p>
            <p><strong>📅 Oluşturulma:</strong> {{ timestamp }}</p>
        </div>
        <a href="/download" class="download-btn">⬇️ Projeyi İndir</a>
        <p style="margin-top: 30px; color: #666;">
            Bu zip dosyası projenizin tüm dosyalarını içerir.<br>
            (.env, database.db ve cache dosyaları hariç)
        </p>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    # Create zip file
    zip_filename = create_zip.create_project_zip()
    
    # Get file info
    file_size = os.path.getsize(zip_filename) / (1024 * 1024)
    timestamp = zip_filename.split('_')[1].split('.')[0]
    formatted_time = f"{timestamp[:4]}-{timestamp[4:6]}-{timestamp[6:8]} {timestamp[9:11]}:{timestamp[11:13]}:{timestamp[13:15]}"
    
    return render_template_string(HTML_TEMPLATE, 
                                filename=zip_filename,
                                size_mb=f"{file_size:.2f}",
                                timestamp=formatted_time)

@app.route('/download')
def download():
    # Find the most recent zip file
    zip_files = [f for f in os.listdir('.') if f.startswith('AiogramShopBot_') and f.endswith('.zip')]
    if not zip_files:
        return "Zip dosyası bulunamadı! Ana sayfaya gidin."
    
    latest_zip = max(zip_files, key=os.path.getctime)
    return send_file(latest_zip, as_attachment=True, download_name=latest_zip)

def open_browser():
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    print("🚀 Download server başlatılıyor...")
    print("📱 Tarayıcınız otomatik olarak açılacak...")
    print("🌐 Manuel erişim: http://localhost:5000")
    
    # Open browser after a short delay
    threading.Timer(1.5, open_browser).start()
    
    app.run(host='0.0.0.0', port=5000, debug=False)
