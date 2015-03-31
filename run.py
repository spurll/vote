#!/usr/bin/env python3

# Written by Gem Newman. This work is licensed under a Creative Commons         
# Attribution-NonCommercial-ShareAlike 3.0 Unported License.                    


from argparse import ArgumentParser

from vote import app


if __name__ == '__main__':
    description = "Runs the Flask server for the voting system."
    parser = ArgumentParser(description=description)
    parser.add_argument("-0", "--public", help="Makes the server world-"
                        "accessible by hosting at 0.0.0.0.",
                        action="store_true")
    parser.add_argument("-p", "--port", help="Defines the port. Defaults to "
                        "9999.", type=int, default=9999)
    parser.add_argument("-d", "--debug", help="Turns server debug mode on. "
                        "(Not recommended for world-accesible servers!)",
                        action="store_true")
    parser.add_argument("-r", "--reload", help="Turns the automatic realoder "
                        "on. This setting restarts the server whenever a "
                        "change in the source is detected.",
                        action="store_true")
    args = parser.parse_args()

    app.run(host="0.0.0.0" if args.public else "localhost", port=args.port,
            use_debugger=args.debug, use_reloader=args.reload)

