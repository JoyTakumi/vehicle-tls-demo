from flask import Flask
import ssl
import os
import logging  # 新增日志模块

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVER_CERT = os.path.join(BASE_DIR, "certs\\server\\server.crt")
SERVER_KEY = os.path.join(BASE_DIR, "certs\\server\\server.key")
CA_CERT = os.path.join(BASE_DIR, "certs\\ca\\ca.crt")

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.minimum_version = ssl.TLSVersion.TLSv1_2
context.load_cert_chain(SERVER_CERT, SERVER_KEY)
context.load_verify_locations(CA_CERT)
context.verify_mode = ssl.CERT_REQUIRED

# 启用详细日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('werkzeug')
logger.setLevel(logging.DEBUG)

@app.route('/')
def hello():
    return "您好，这是一个安全的汽车云平台！"

if __name__ == '__main__':
    app.run(
        host="localhost",
        port=5000,
        ssl_context=context,
        debug=True
    )
