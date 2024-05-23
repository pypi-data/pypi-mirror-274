from heiwa4126_hello_python.main import hello


def test_hello(capsys):
    hello()
    captured = capsys.readouterr()
    assert (
        captured.out
        == "Hello world!\nGood-bye cruel world!\n(1, 2, 3, 4)\nIn olden days, a glimpse of stocking\nWas looked on as something shocking.\nBut now, God knows, Anything goes.\nGood authors too who once knew better words\nNow only use four-letter words\nWriting prose.\nAnything goes. \n(5, 6, 7, 8)\n"
    )
