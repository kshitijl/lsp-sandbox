import json
import sys
import time


def main():
    with open("/tmp/recsand.log", "a") as f:
        f.write("opened for writing\n")
        f.flush()
        # content_length_line = sys.stdin.readline()
        # tokens =

        # for line in sys.stdin.readlines():
        #     f.write(line)
        #     f.flush()

        while True:
            content_length_line = sys.stdin.readline()

            if not content_length_line:
                break
            f.write(content_length_line)
            f.flush()

            _, num_bytes = content_length_line.split(" ")
            num_bytes = int(num_bytes)

            content = sys.stdin.read(num_bytes + 2)
            f.write("read chunk\n")

            f.write("read {} bytes\n".format(len(content)))
            f.flush()
            # decoded = chunk.decode()
            f.write(content)
            f.flush()

        f.write("done bye\n")
        f.flush()


if __name__ == "__main__":
    main()
