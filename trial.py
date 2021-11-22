import sys

argv = sys.argv

print(f"\nThere are {len(argv)} list elements in sys.argv: \n")
for index, e in enumerate(argv):
    print(f"sys.argv[{index}]: {e}")