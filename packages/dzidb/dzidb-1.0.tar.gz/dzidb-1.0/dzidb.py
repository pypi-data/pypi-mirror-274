import argparse

def main():
    parser = argparse.ArgumentParser(description='Custom adb-like tool.')
    parser.add_argument('command', help='Command to execute.')
    args = parser.parse_args()

    if args.command == 'help' :
        print("Custom help documentation goes here.")
    else:
        print(f"Unknown command: {args.command}")

if __name__ == '__main__':
    main()