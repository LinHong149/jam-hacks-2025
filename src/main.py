import setup
import playlist
import os
import sys

def print_menu():
    print("1. Create new playlist")
    print("2. Sync existing playlist")
    print("3. Delete playlist")
    print("4. Download playlist")
    print("5. Convert playlist to lofi")
    return int(input())


def main():
    # setup.create_directory()
    # setup.setupenv()
    # while True:
    choice = print_menu()
    match choice:
        case 1: # create new playlist
            playlist.create()
        case 2: # sync existing playlist
            playlist.update()
        case 5: # convert to lofi
            playlist.convert()



if __name__ == "__main__":
    main()
