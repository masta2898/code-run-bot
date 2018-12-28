import logging
import sys
import subprocess
from io import StringIO
import contextlib
import traceback


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
        self._history = []

    def code_run(self, code):
        logging.info(f'Code input: {code}')

        try:
            with stdoutIO() as s:
                try:
                    result = eval(code, self.globals, self.locals)
                    if result:
                        self._history.append(code)
                        return result

                except SyntaxError:
                    exec(code, self.globals, self.locals)
                    self._history.append(code)

            return s.getvalue()

        except Exception as ex:
            logging.exception(ex)
            return f'Error:\n {traceback.format_exc()}'

    def add_library(self, lib_name):
        result = subprocess.run(['pip', 'install', lib_name], stdout=subprocess.PIPE)
        return result.stdout.decode('utf-8')

    def history(self):
        return '\n'.join(self._history)


if __name__ == '__main__':
    sess = CodingSession()
    logging.basicConfig(level=logging.DEBUG)
    #res = sess.add_library('requests')

    logging.debug(sess.code_run('a=1\nb=2'))
    logging.debug(sess.code_run('b'))
    logging.debug(sess.code_run('print("3")'))
    logging.debug(sess.code_run('2'))

    logging.debug(sess.code_run(sess.history()))

    sess.clear()

    logging.debug(sess.code_run('b'))
    # logging.debug(sess.code_run('__'))
