import argparse
import json
from xssbase import scan_website

def main():
    parser = argparse.ArgumentParser(
        description='XSSBase: A professional tool for scanning XSS vulnerabilities.',
        epilog='Copyright (c) 2024 Author Fidal'
    )
    parser.add_argument('--url', required=True, help='The base URL of the website to scan.')
    parser.add_argument('--payload', help='A custom XSS payload to use instead of the default payloads.')
    parser.add_argument('--headers', help='Custom headers to include in the requests (JSON format).')
    parser.add_argument('--methods', help='HTTP methods to use for testing (comma-separated, e.g., "GET,POST").')

    args = parser.parse_args()

    if args.payload:
        payloads = [args.payload]
    else:
        payloads = None

    if args.headers:
        try:
            headers = json.loads(args.headers)
        except json.JSONDecodeError:
            print("Invalid JSON format for headers. Please provide valid JSON.")
            return
    else:
        headers = None

    if args.methods:
        methods = [method.lower() for method in args.methods.split(',')]
    else:
        methods = None

    vulnerabilities = scan_website(args.url, payloads, methods, headers)
    print("Vulnerabilities found:")
    for vuln in vulnerabilities:
        print(vuln)

if __name__ == '__main__':
    main()
      
