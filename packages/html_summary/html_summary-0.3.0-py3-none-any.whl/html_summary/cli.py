import os
import tempfile

import click
import httpx
from dotenv import find_dotenv
from dotenv import load_dotenv
from loguru import logger

from .summary import load_html
from .summary import load_pdf
from .summary import summarize


def fetch_content(path: str) -> str:
    if path.startswith("http"):
        resp = httpx.get(url=path)
        resp.raise_for_status()

        with tempfile.NamedTemporaryFile(delete=False) as fp:
            fp.write(resp.content)
            f = fp.name
    else:
        f = path
    return f


@click.command()
@click.argument("path", type=click.STRING)
@click.option("-l", "--lang", type=click.STRING, default="English")
@click.option("--pdf", is_flag=True, type=click.BOOL)
def main(path: str, lang: str, pdf: bool) -> None:
    load_dotenv(find_dotenv())

    lang = os.getenv("HTML_SUMMARY_LANG", lang)

    f = fetch_content(path)

    text = load_pdf(f) if pdf else load_html(f)
    s = summarize(text, lang)
    logger.info("summarization:\n{}", s)
