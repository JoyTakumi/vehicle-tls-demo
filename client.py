import requests
import os
from requests.exceptions import SSLError

# 证书路径配置（Windows路径格式）
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CERT_DIR = os.path.join(BASE_DIR, "certs")

# 证书文件路径
CA_CERT = os.path.join(CERT_DIR, "ca\\ca.crt")
VALID_CERT = (
    os.path.join(CERT_DIR, "client\\client.crt"),
    os.path.join(CERT_DIR, "client\\client.key")
)
INVALID_CERT = (
    os.path.join(CERT_DIR, "invalid\\invalid_client.crt"),
    os.path.join(CERT_DIR, "invalid\\invalid_client.key")
)

def print_banner(scenario_num, description):
    """打印带边框的测试场景标题"""
    print(f"\n{'='*40}")
    print(f" 测试场景 {scenario_num}: {description} ")
    print(f"{'='*40}")

def test_connection(cert=None, verify=CA_CERT):
    """执行HTTPS请求并返回格式化结果"""
    try:
        response = requests.get(
            "https://localhost:5000",
            cert=cert,
            verify=verify,
            timeout=5
        )
        return {
            "status": "✅ 连接成功",
            "code": response.status_code,
            "content": response.text.strip()
        }
    except SSLError as e:
        return {
            "status": "🔒 SSL握手失败",
            "error": str(e).split(']')[-1].strip()
        }
    except Exception as e:
        return {
            "status": "❌ 意外错误",
            "error": str(e)
        }

def print_result(result):
    """格式化打印测试结果"""
    print("\n[ 测试结果 ]")
    print(f"状态: {result['status']}")
    if 'code' in result:
        print(f"状态码: {result['code']}")
        print(f"响应内容: {result['content']}")
    else:
        print(f"错误详情: {result['error']}")
    print("-"*40)

if __name__ == '__main__':
    # 场景1：有效证书
    print_banner(1, "使用合法客户端证书")
    result = test_connection(cert=VALID_CERT)
    print_result(result)

    # 场景2：无效证书
    print_banner(2, "使用非法客户端证书")
    result = test_connection(cert=INVALID_CERT)
    print_result(result)

    # 场景3：无证书
    print_banner(3, "不提供客户端证书")
    result = test_connection(cert=None)
    print_result(result)
