import argparse
import requests
import os
import sys


def main():
    parser = argparse.ArgumentParser(description="Send a PDF file to the OCR service")
    parser.add_argument("file", help="Path to the PDF file to be processed")
    parser.add_argument(
        "--server",
        default="http://localhost:8080",
        help="Server URL (default: http://localhost:8080)",
    )

    args = parser.parse_args()

    if not os.path.isfile(args.file):
        print(f"Error: File '{args.file}' does not exist")
        sys.exit(1)

    if not args.file.lower().endswith(".pdf"):
        print("Warning: The file does not have a .pdf extension")

    url = f"{args.server}/ocr"

    try:
        with open(args.file, "rb") as f:
            files = {"file": (os.path.basename(args.file), f, "application/pdf")}

            # Disable proxies for local requests
            proxies = {"http": "", "https": ""}
            response = requests.post(url, files=files, proxies=proxies)

        if response.status_code == 200:
            print("File successfully processed")
            print(response.json())
        else:
            print(f"Error: Server returned status code {response.status_code}")
            print(response.text)

    except requests.exceptions.ConnectionError as e:
        print(f"Error: Could not connect to server at {args.server} because of {e}")
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
