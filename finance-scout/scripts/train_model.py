from __future__ import annotations

import argparse


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=False, help="Path to labeled training data")
    args = parser.parse_args()
    print("ML training is optional. Provide labeled data to implement training.")
    if args.data:
        print(f"Data provided: {args.data}")


if __name__ == "__main__":
    main()
