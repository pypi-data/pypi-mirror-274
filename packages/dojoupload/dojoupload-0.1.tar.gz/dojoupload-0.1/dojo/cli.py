import argparse
from dojo.main import main as dojo_main

def parse_arguments():
    parser = argparse.ArgumentParser(description='Dojo Upload CLI')
    parser.add_argument('url', help='Base URL of the Dojo instance')
    parser.add_argument('token', help='Authorization token for the Dojo instance')
    parser.add_argument('product_name', help='Name of the product')
    parser.add_argument('engagement_name', help='Name of the engagement')
    parser.add_argument('file_path', help='Path to the file to be uploaded')
    parser.add_argument('scan_type', help='Type of scan')

    return parser.parse_args()

def main():
    args = parse_arguments()
    url = args.url
    token = args.token
    product_name = args.product_name
    engagement_name = args.engagement_name
    file_path = args.file_path
    scan_type = args.scan_type

    dojo_main(url, token, product_name, engagement_name, file_path, scan_type)

if __name__ == '__main__':
    main()
