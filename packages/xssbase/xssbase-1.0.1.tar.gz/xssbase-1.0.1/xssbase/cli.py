import argparse
import sys
from xssbase import scan_website, save_to_file_func, get_vulnerability_details

class CustomHelpFormatter(argparse.HelpFormatter):
    def format_help(self):
        help_text = super().format_help()
        help_text += "\nCopyright (c) 2024 author Fidal\n"
        return help_text

def main():
    parser = argparse.ArgumentParser(
        description="XSS scanning tool",
        formatter_class=CustomHelpFormatter
    )
    parser.add_argument('--url', required=True, help='Base URL of the website to scan')
    parser.add_argument('--payload', help='Custom XSS payload')
    parser.add_argument('--methods', nargs='+', default=['get', 'post'], help='HTTP methods to use for scanning (default: get post)')
    parser.add_argument('--headers', nargs='+', help='Custom headers for the requests')
    parser.add_argument('-s', '--save', help='File to save the scan results')
    
    args = parser.parse_args()
    
    url = args.url
    custom_payloads = [args.payload] if args.payload else None
    methods = args.methods
    headers = dict(header.split(':') for header in args.headers) if args.headers else None
    save_to_file = args.save
    
    vulnerabilities = scan_website(url, custom_payloads, methods, headers, save_to_file)
    
    if save_to_file:
        save_to_file_func(save_to_file, get_vulnerability_details(vulnerabilities))

if __name__ == '__main__':
    main()
