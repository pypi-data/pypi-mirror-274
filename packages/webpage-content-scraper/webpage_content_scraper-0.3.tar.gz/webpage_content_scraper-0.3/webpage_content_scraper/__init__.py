from typing import List, Union

from bs4 import BeautifulSoup, NavigableString, Tag
from playwright.sync_api import sync_playwright, TimeoutError
from markdownify import MarkdownConverter


class Formats:
    MARKDOWN = 'markdown'
    HTML = 'html'


def _get_reader_content(html: str) -> Union[Tag, NavigableString]:
    soup = BeautifulSoup(html, 'html.parser')
    reader_content = soup.find(class_='moz-reader-content')

    return reader_content if reader_content and reader_content.contents else None


def fetch_page_content(
    urls: List[str], format: str = Formats.HTML, timeout: int = 10
) -> List[Union[str, None]]:
    if not isinstance(urls, list) or not all(isinstance(url, str) for url in urls):
        raise ValueError('urls must be a list of strings')

    pages_content: List[Union[str, None]] = []

    with sync_playwright() as p:
        browser = p.firefox.launch()
        page = browser.new_page()

        for url in urls:
            try:
                page.goto(f'about:reader?url={url}', timeout=timeout * 1000)
                page.wait_for_selector('.moz-reader-content *', timeout=timeout * 1000)

                html = page.content()
                reader_content = _get_reader_content(html)

                if not reader_content:
                    pages_content.append('')
                    continue

                if format == Formats.MARKDOWN:
                    pages_content.append(
                        MarkdownConverter(
                            heading_style='ATX', heading_level=2
                        ).convert_soup(reader_content)
                    )
                else:
                    pages_content.append(str(reader_content))
            except TimeoutError:
                pages_content.append('')
            except Exception as e:
                pages_content.append(f'Error: {e}')

        browser.close()

    return pages_content
