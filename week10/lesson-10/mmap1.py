import imp
import mmap
import os

def mmap_io_display_lines(filename):
    with open(filename, mode='r', encoding='utf8') as file_obj:
        with mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_READ) as map_file:
        # if length is set to 0 it will do the full file but can be dangerous/problamatic if file is to big
            for line in iter(map_file.readline, b""):
                print(line)

            # find last character on file
            map_file.seek(-1, os.SEEK_END) #mmap always have 'x' as last line to indicte end of file so have to do 
            print(f"last character in file is '{map_file.read(1).decode()}'") #decode makes binary into letter

def main():
    mmap_io_display_lines('data.txt')

if __name__ == '__main__':
    main()