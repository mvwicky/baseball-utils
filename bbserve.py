import os

from baseball_utils import create_app


def main(dev: bool = True, debug: bool = True):
    if dev:
        os.environ['FLASK_ENV'] = 'development'
    else:
        os.environ['FLASK_ENV'] = 'production'

    os.environ['FLASK_DEBUG'] = str(debug)

    app = create_app()
    app.run(threaded=True)


if __name__ == '__main__':
    main()
