import json
import sys


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

            parsed = json.loads(content)

            if "method" in parsed:
                method = parsed["method"]

                if method == "textDocument/hover":
                    id = parsed["id"]
                    response = {
                        "jsonrpc": "2.0",
                        "id": id,
                        "result": {
                            "contents": {
                                "kind": "markdown",
                                "value": "# Do programming!\nIt's fun.\n## Do it\nAll day *every* day",
                            }
                        },
                    }

                    send_response(response, f)

                if method == "textDocument/didChange":
                    file_contents = (
                        parsed["params"]["contentChanges"][0]["text"]
                        .lower()
                        .split("\n")
                    )
                    diagnostics = []
                    for index, line in enumerate(file_contents):
                        bad_word = "oops"
                        if bad_word in line.lower():
                            offset = line.find(bad_word)
                            diagnostics.append(
                                {
                                    "message": "bad!!!",
                                    "severity": 1,
                                    "source": "recsand-lsp",
                                    "range": {
                                        "start": {"character": offset, "line": index},
                                        "end": {
                                            "line": index,
                                            "character": offset + len(bad_word),
                                        },
                                    },
                                }
                            )

                    uri = parsed["params"]["textDocument"]["uri"]
                    version = parsed["params"]["textDocument"]["version"]
                    response = {
                        "jsonrpc": "2.0",
                        "method": "textDocument/publishDiagnostics",
                        "params": {
                            "uri": uri,
                            "version": version,
                            "diagnostics": diagnostics,
                        },
                    }
                    send_response(response, f)
                if parsed["method"] == "exit":
                    f.write("exit bye")
                    break

                if parsed["method"] == "shutdown":
                    id = parsed["id"]
                    response = {"jsonrpc": "2.0", "id": id, "result": None}

                    send_response(response, f)
                if parsed["method"] == "initialize":
                    id = parsed["id"]
                    response = {
                        "jsonrpc": "2.0",
                        "id": id,
                        "result": {
                            "capabilities": {
                                "diagnosticProvider": {
                                    "identifier": "recsand-lsp",
                                    "interFileDependencies": False,
                                    "workDoneProgress": False,
                                    "workspaceDiagnostics": False,
                                },
                                "textDocumentSync": {
                                    "change": 1,
                                    "openClose": True,
                                    "willSave": False,
                                },
                                "hoverProvider": {},
                            }
                        },
                    }

                    send_response(response, f)

            f.flush()

        f.write("done bye\n")
        f.flush()


def send_response(response: dict, f):
    response_json = json.dumps(response)
    response_length = len(response_json)
    actual_response = "Content-Length: {}\r\n\r\n{}".format(
        response_length, response_json
    )
    f.write("sending back {}\n".format(actual_response))
    sys.stdout.write(actual_response)
    # sys.stdout.write(actual_response)
    sys.stdout.flush()


if __name__ == "__main__":
    main()
