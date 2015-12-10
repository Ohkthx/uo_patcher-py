import urllib.request as urlrequest
import sys
from time import sleep
from subprocess import Popen
from os import name as os_name


def main(url):
    sleep(2.0)                              # Allow time for program to exit.
    file_name = url.split('/')[-1]          # Grab the file name.
    try:
        remote_file = urlrequest.urlopen(url)   # Open the remote end.
        local_file = open(file_name, 'wb')      # Set object for local file
    
        file_size = float(remote_file.headers['Content-Length'])    
        print("  Downloading: %s\n Size: %.2fMB" % (file_name, file_size/(1024.0 * 1024.0)))

        block_size = 8192
        file_size_dl = 0

        while True:
            buffer = remote_file.read(block_size)
            if not buffer:
                break

            file_size_dl += len(buffer)
            local_file.write(buffer)

            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
            status = status + chr(8)*(len(status)+1)
            print(status)

        local_file.close()

        print("Download complete.\nRelaunching: %s" % file_name)
        sleep(2.0)
        if os_name != 'nt':
            file_name = './' + file_name

        Popen([file_name])
    except IOError as err:
        print("  [ ERROR ]  IO Error: [Code: %s, %s]" % (err.errno, err.strerror))
        if os_name == 'nt':
            input(" Press any key to exit...")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("URL not passed.")
        sys.exit()
    else:
        main(sys.argv[1])
