from typing import Tuple, List


def decode_message(message: str) -> Tuple[str, List[str]]:
    args = message.split(" ")
    cmd = args.pop(0)

    return cmd, args
