from subprocess import PIPE, Popen


def _process(command):
    p = Popen(command, stdout=PIPE, stdin=PIPE, shell=True)
    out, err = p.communicate()
    if p.returncode != 0:
        return False
    return True


def test_black():
    assert _process(["black", "--check", "./vectorback"])


def test_flake8():
    assert _process(["flake8", "./vectorback"])


def test_isort():
   assert _process(["isort", "--check", "./vectorback"])