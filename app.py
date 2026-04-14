from flask import Flask, render_template, request, jsonify
import socket
import requests

app = Flask(__name__)

# Resolve domain → IP
def get_ip(domain):
    try:
        return socket.gethostbyname(domain)
    except:
        return "Unable to resolve"

# Scan common ports
def scan_ports(ip):
    common_ports = [21, 22, 23, 25, 53, 80, 443]
    open_ports = []

    for port in common_ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(0.5)
        result = sock.connect_ex((ip, port))
        if result == 0:
            open_ports.append(port)
        sock.close()

    return open_ports

# Get HTTP headers
def get_headers(url):
    try:
        response = requests.get(url, timeout=3)
        return dict(response.headers)
    except:
        return {"error": "Could not fetch headers"}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    data = request.json
    target = data['target']

    ip = get_ip(target)
    ports = scan_ports(ip) if ip != "Unable to resolve" else []
    headers = get_headers("http://" + target)

    return jsonify({
        "ip": ip,
        "ports": ports,
        "headers": headers
    })

if __name__ == '__main__':
    app.run(debug=True)