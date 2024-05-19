import sys
import textwrap

from . import meta


def main():

    assert 'NAME'    not in globals()
    assert 'VERSION' not in globals()

    exec(meta.get_meta_str())

    assert 'NAME'    in globals()
    assert 'VERSION' in globals()

    assert 'mychamp' == NAME

    sys.stderr.write(
        textwrap.dedent(
            f'''\
            {NAME} {VERSION}

                usage: python -m {NAME}.<train|predict> [-h] [...]

            '''
        )
    )
    return 1 # error: improper usage


if '__main__' == __name__:
    sys.exit(main())


