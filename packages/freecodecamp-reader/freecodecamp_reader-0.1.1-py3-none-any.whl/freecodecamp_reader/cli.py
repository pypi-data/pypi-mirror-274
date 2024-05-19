import argparse
from .parser import get_latest_tutorials

def main():
    parser = argparse.ArgumentParser(description='Fetch the latest tutorials from FreeCodeCamp News.')
    parser.add_argument('--count', type=int, default=5, help='Number of latest tutorials to fetch')
    args = parser.parse_args()

    try:
        tutorials = get_latest_tutorials(args.count)
        for tutorial in tutorials:
            print(tutorial)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
