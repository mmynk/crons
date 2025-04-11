import argparse
import os

from currency import send_currency_alert

def load_env():
    if not os.path.exists(".env"):
        return
    with open(".env", "r") as f:
        for line in f:
            key, value = line.strip().split("=")
            os.environ[key] = value


def main():
    load_env()

    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest="command")

    currency_parser = subparsers.add_parser("currency")
    currency_parser.add_argument("-s", "--source", type=str, required=True, help="Source currency")
    currency_parser.add_argument("-t", "--target", type=str, required=True, help="Target currency")
    currency_parser.add_argument("-e", "--email", type=str, required=False, default=None, help="Alert email")

    args = parser.parse_args()

    if args.command == "currency":
        send_currency_alert(args.source, args.target, args.email)


if __name__ == "__main__":
    main()
