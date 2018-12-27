import logging
import sys
from io import StringIO
import contextlib


@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old


class CodingSession:
    def __init__(self):
        self.globals = globals().copy()
        self.locals = locals().copy()

    def code_run(self, code):
        logging.info(f'Code input: {code}')

        try:
            with stdoutIO() as s:
                try:
                    result = eval(code, self.globals, self.locals)
                    if result:
                        return result

                except SyntaxError:
                    exec(code, self.globals, self.locals)

            return s.getvalue()

        except Exception as ex:
            logging.exception(ex)
            return f'Error:\n {sys.exc_info()}'


if __name__ == '__main__':
    sess = CodingSession()
    logging.basicConfig(level=logging.DEBUG)

    logging.debug(sess.code_run('a=1\nb=2'))
    logging.debug(sess.code_run('b'))
    logging.debug(sess.code_run('print("3")'))
    logging.debug(sess.code_run('2'))
    logging.debug(sess.code_run('__'))
