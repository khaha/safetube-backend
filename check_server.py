import socket
import time
import subprocess
import os

def check_port(host='127.0.0.1', port=54053, timeout=2):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

def start_server():
    # Kiểm tra xem server đã chạy chưa
    if check_port():
        print("✅ VnCoreNLP server is already running on port 54053")
        return True

    # Nếu chưa, khởi động server
    print("🚀 Starting VnCoreNLP server...")
    jar_path = "VnCoreNLP-1.1.1.jar"
    if not os.path.exists(jar_path):
        print("❌ VnCoreNLP JAR file not found. Please download it.")
        return False

    # Chạy server trong background
    process = subprocess.Popen([
        "java", "-Xmx2g", "-jar", jar_path,
        "-port", "54053", 
        "-annotators", "wseg,pos,ner,parse"
    ])

    # Chờ server khởi động
    for i in range(30):
        if check_port():
            print("✅ VnCoreNLP server started successfully!")
            return True
        time.sleep(1)

    print("❌ Failed to start VnCoreNLP server within 30 seconds")
    return False

if __name__ == "__main__":
    start_server()
