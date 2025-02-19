import uvicorn

from config import config


def main():

    uvicorn.run (

        app='app:app',
        host=config.host,
        port=config.port,
        reload=config.reload
    )


if __name__ == '__main__':
    main()