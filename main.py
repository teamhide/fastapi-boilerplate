import os

import click
import uvicorn

from core.config import config


@click.command()
@click.option(
    "--stage",
    type=click.Choice(["local", "dev", "prod"], case_sensitive=False),
    default="local",
)
def main(stage: str):
    os.environ["STAGE"] = stage

    uvicorn.run(
        app="app.server:app",
        host=config.APP_HOST,
        port=config.APP_PORT,
        reload=True if config.ENV != "production" else False,
        workers=1,
    )


if __name__ == "__main__":
    main()
