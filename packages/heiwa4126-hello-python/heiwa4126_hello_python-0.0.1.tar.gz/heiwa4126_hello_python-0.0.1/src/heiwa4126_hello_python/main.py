#!/usr/bin/env python3
"""
Python の動作テスト兼テンプレート
兼 VScode の debug の構成作成
兼 hatch のテスト
"""


def hello() -> None:
    """
    This is the main function of the program.
    It prints out various messages and tuples.
    """
    print("Hello world!")
    print("Good-bye cruel world!")
    print((1, 2, 3, 4))
    print(
        """In olden days, a glimpse of stocking
Was looked on as something shocking.
But now, God knows, Anything goes.
Good authors too who once knew better words
Now only use four-letter words
Writing prose.
Anything goes. """
    )
    print((5, 6, 7, 8))


if __name__ == "__main__":
    hello()
