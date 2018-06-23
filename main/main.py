import os
from application.application import App

APP_DIR = os.path.dirname(os.path.realpath(__file__))
DEFAULT_DIR = 'C:/Users/'

if __name__ == '__main__':
    print(APP_DIR)
    app = App(None, APP_DIR)
    app.title('Will you just show up')
    app.mainloop()


