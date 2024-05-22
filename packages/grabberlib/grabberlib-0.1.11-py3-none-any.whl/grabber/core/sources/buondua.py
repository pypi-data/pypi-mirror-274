import pathlib
from typing import Dict, List, Optional
from urllib.parse import urljoin

from lxml import etree
from telegraph import Telegraph
from tqdm import tqdm

from grabber.core.utils import (
    downloader,
    get_soup,
    get_tags,
    headers_mapping,
    query_mapping,
    query_pagination_mapping,
    telegraph_uploader,
)


def get_pages_from_pagination(
    url: str,
    target: str,
    headers: Optional[Dict[str, str]] = None,
) -> List[str]:
    pagination_params = query_pagination_mapping[target]
    source_urls = set()
    soup = get_soup(url, headers=headers)
    dom = etree.HTML(str(soup))
    pagination_set = soup.select(pagination_params.pages_count_query)

    if not pagination_set:
        for a_tag in dom.xpath(pagination_params.posts_query_xpath):
            if a_tag is not None and a_tag.attrib["href"] not in source_urls:
                source_urls.add(a_tag.attrib["href"])
        return source_urls

    base_pagination_url = url.rsplit("/", 1)[0]
    for a_tag in dom.xpath(pagination_params.posts_query_xpath):
        page_link = a_tag.attrib["href"]
        target_url = urljoin(base_pagination_url, page_link)
        source_urls.add(target_url)

    return list(source_urls)


def get_sources_for_buondua(
    sources: List[str],
    entity: str,
    telegraph_client: Optional[Telegraph] = None,
    final_dest: str | pathlib.Path = "",
    save_to_telegraph: bool | None = False,
    is_tag: Optional[bool] = False,
    limit: Optional[int] = None,
) -> None:
    tqdm_sources_iterable = tqdm(
        enumerate(sources),
        total=len(sources),
        desc="Retrieving URLs...",
    )
    query, src_attr = query_mapping[entity]
    headers = headers_mapping.get(entity, None)
    page_title = None
    title_folder_mapping = {}
    posts_sent_counter = 0
    titles = []

    if final_dest:
        final_dest = pathlib.Path(final_dest)
        if not final_dest.exists():
            final_dest.mkdir(parents=True, exist_ok=True)

    for idx, source_url in tqdm_sources_iterable:
        folder_name = ""
        urls = [
            source_url,
            *get_pages_from_pagination(url=source_url, target="buondua", headers=headers),
        ]
        image_tags = []

        for index, url in enumerate(urls):
            tags, soup = get_tags(
                url,
                headers=headers,
                query=query,
            )
            image_tags.extend(tags or [])

            if index == 0 or page_title is None:
                page_title = soup.find("title").get_text(strip=True)
                folder_name = page_title
                titles.append(page_title)

        unique_img_urls = set()
        for idx, img_tag in enumerate(image_tags):
            img_src = img_tag.attrs[src_attr]
            img_name: str = img_src.split("/")[-1].split("?")[0]
            img_name = img_name.strip().rstrip()
            unique_img_urls.add((f"{idx + 1}-{img_name}", img_src))

        tqdm_sources_iterable.set_description(f"Finished retrieving images for {page_title}")

        if final_dest:
            folder_name = page_title
            title_dest = final_dest / folder_name
            if not title_dest.exists():
                title_dest.mkdir(parents=True, exist_ok=True)
            title_folder_mapping[page_title] = (unique_img_urls, title_dest)

        if save_to_telegraph:
            telegraph_uploader(
                unique_img_urls=unique_img_urls,
                page_title=page_title,
                posts_sent_counter=posts_sent_counter,
                telegraph_client=telegraph_client,
                tqdm_iterable=tqdm_sources_iterable,
            )
            posts_sent_counter += 1
        page_title = None

    if final_dest:
        downloader(
            titles=titles,
            title_folder_mapping=title_folder_mapping,
            headers=headers,
        )
