import logging


class CodingSession:
    def __init__(self):
        self.globals = globals().copy()
        self.locals = locals().copy()

    def code_run(self, code):
        exec(code, self.globals, self.locals)

        try:
            return eval(code, self.globals,self.locals)
        except:
            pass

if __name__ == '__main__':
    sess = CodingSession()
    logging.basicConfig(level=logging.DEBUG)

    logging.debug(sess.code_run('a=1'))
    logging.debug(sess.code_run('a'))
    logging.debug(sess.code_run('print(a)'))
    logging.debug(sess.code_run('2'))
