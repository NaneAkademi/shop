
#!/usr/bin/env python3
import subprocess
import sys
import os

def main():
    print("🤖 AiogramShopBot Proje İndirme Aracı")
    print("=" * 50)
    
    try:
        # Check if Flask is installed
        import flask
        print("✅ Flask yüklü")
    except ImportError:
        print("📦 Flask yükleniyor...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
    
    print("\n🔄 Zip dosyası oluşturuluyor ve download server başlatılıyor...")
    print("📱 Tarayıcınız otomatik olarak açılacak")
    print("🌐 Manuel erişim: http://localhost:5000")
    print("\nServer'ı durdurmak için Ctrl+C kullanın\n")
    
    # Start the download server
    os.system("python download_server.py")

if __name__ == "__main__":
    main()
