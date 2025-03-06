from utils.custom_requests import CustomRequests
from hashlib import md5
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64decode
import json
import importlib
import os


def __sync_cookiecloud(server_host: str, user_key: str, password: str):
    # 这里添加同步 CookieCloud 的逻辑
    url = f"{server_host[:-1] if server_host.endswith('/') else server_host}/get/{user_key}"
    print("Syncing cookies from cookiecloud...")
    rsp = CustomRequests.get(url)
    encrypted = b64decode(rsp.json().get('encrypted', False))

    key = md5(f"{user_key}-{password}".encode()
              ).hexdigest()[:16].encode()
    salt = encrypted[8:16]
    ct = encrypted[16:]

    # 使用OpenSSL EVP_BytesToKey导出方式
    key_iv = b""
    prev = b""
    while len(key_iv) < 48:
        prev = md5(prev + key + salt).digest()
        key_iv += prev

    _key = key_iv[:32]
    _iv = key_iv[32:48]

    # 创建cipher并解密
    cipher = AES.new(_key, AES.MODE_CBC, _iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return json.loads(pt.decode('utf-8')).get("cookie_data", {})


def fetch_cookie(sites: dict):
    # 从环境变量中获取server_host, user_key, password
    server_host = os.environ.get('COOKIECLOUD_SERVER_URL')
    user_key = os.environ.get('COOKIECLOUD_USER_KEY')
    password = os.environ.get('COOKIECLOUD_SERVER_PASSWORD')
    if not server_host or not user_key or not password:
        raise Exception("Missing CookieCloud environment variables")

    dc_data = __sync_cookiecloud(server_host, user_key, password)
    for site_name in sites.keys():
        module = importlib.import_module(f'nexus.{site_name}')
        site_class = getattr(module, site_name)
        site_url = site_class.get_url()
        site_host = site_url.replace("https://", "").replace("http://", "").split("/")[0]
        cookieStr = ""
        for cookie in dc_data.get(site_host, {}):
            try:
                cookieStr += f"{cookie['name']}={cookie['value']};"
            except:
                continue
        print(site_name, site_url, cookieStr)
        sites[site_name]['cookie'] = cookieStr
    return sites
