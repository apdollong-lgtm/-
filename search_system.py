"""ระบบค้นหาข้อมูลออนไลน์แบบเรียบง่ายด้วย Wikipedia OpenSearch API."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List
from urllib.parse import quote
from urllib.request import urlopen
import json


@dataclass
class SearchResult:
    """ผลลัพธ์การค้นหา 1 รายการ"""

    title: str
    snippet: str
    url: str


class SearchError(Exception):
    """เกิดข้อผิดพลาดระหว่างค้นหาข้อมูลออนไลน์"""


def _build_wikipedia_url(query: str, limit: int) -> str:
    encoded = quote(query)
    return (
        "https://th.wikipedia.org/w/api.php"
        f"?action=opensearch&search={encoded}&limit={limit}&namespace=0&format=json"
    )


def search_online(query: str, max_results: int = 5) -> List[SearchResult]:
    """ค้นหาข้อมูลออนไลน์จาก Wikipedia

    Args:
        query: คำค้นหา
        max_results: จำนวนผลลัพธ์สูงสุด

    Returns:
        รายการ SearchResult

    Raises:
        ValueError: หาก query ว่าง หรือ max_results ไม่ถูกต้อง
        SearchError: หากเรียก API ไม่สำเร็จหรือข้อมูลผิดรูปแบบ
    """

    query = query.strip()
    if not query:
        raise ValueError("query ต้องไม่ว่าง")
    if max_results <= 0:
        raise ValueError("max_results ต้องมากกว่า 0")

    url = _build_wikipedia_url(query, max_results)

    try:
        with urlopen(url, timeout=10) as response:  # nosec B310
            payload = response.read().decode("utf-8")
        data = json.loads(payload)
    except Exception as exc:  # pragma: no cover
        raise SearchError(f"ไม่สามารถค้นหาข้อมูลออนไลน์ได้: {exc}") from exc

    if not isinstance(data, list) or len(data) < 4:
        raise SearchError("ข้อมูลจาก API ไม่ถูกต้อง")

    titles = data[1]
    snippets = data[2]
    urls = data[3]

    results: List[SearchResult] = []
    for title, snippet, link in zip(titles, snippets, urls):
        results.append(SearchResult(title=title, snippet=snippet, url=link))

    return results


def format_results(results: List[SearchResult]) -> str:
    """แปลงผลลัพธ์ให้อยู่ในรูปแบบข้อความอ่านง่าย"""

    if not results:
        return "ไม่พบผลลัพธ์"

    lines = []
    for index, result in enumerate(results, start=1):
        lines.append(f"{index}. {result.title}")
        lines.append(f"   {result.snippet}")
        lines.append(f"   {result.url}")
    return "\n".join(lines)
