import logging
import sys
from io import StringIO
import contextlib


class CodingSession:
    def __init__(self):
        self.globals = globals().copy()
        self.locals = locals().copy()

    def code_run(self, code):
        @contextlib.contextmanager
        def stdoutIO(stdout=None):
            old = sys.stdout
            if stdout is None:
                stdout = StringIO()
            sys.stdout = stdout
            yield stdout
            sys.stdout = old

        with stdoutIO() as s:
            try:
                result = eval(code, self.globals,self.locals)
                if result:
                    return result

            except SyntaxError:
                exec(code, self.globals, self.locals)

        return s.getvalue()


if __name__ == '__main__':
    sess = CodingSession()
    logging.basicConfig(level=logging.DEBUG)

    logging.debug(sess.code_run('a=1'))
    logging.debug(sess.code_run('a'))
    logging.debug(sess.code_run('print("3")'))
    logging.debug(sess.code_run('2'))
