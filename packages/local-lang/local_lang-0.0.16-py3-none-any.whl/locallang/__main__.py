#  Copyright (c) 2024 pieteraerens.eu
#  All rights reserved.
#  The file __main__.py is a part of localisation.
#  Created by harrypieteraerens
#  Created: 4/28/24, 2:18 AM
#  Last modified: 4/28/24, 2:18 AM

import argparse

from locallang import LangInit, __version__


def main():
    parser = argparse.ArgumentParser(description="Reload the localization")
    parser.add_argument("--default-local", type=str, default="en_us", help="Default localisation")
    parser.add_argument("--version", action="version", version=f"local-lang version {__version__}")

    args = parser.parse_args()

    if args.default_local:
        print("""
Starting the localisation reload
        """)
        lang_init = LangInit(default_language=args.default_local)
        lang_init.reload_localization()
        print("""
Localisation reloaded
        """)

    else:
        print("Please provide the default localisation")
        exit(1)


if __name__ == "__main__":
    main()
