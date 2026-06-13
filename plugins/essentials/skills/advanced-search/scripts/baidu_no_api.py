#!/usr/bin/env python3
"""
百度搜索引擎 — 无需 API Key
通过 www.baidu.com 网页抓取获取搜索结果。作为 Baidu MCP (baidu_web_search) 不可用时的兜底方案。

用法:
  python baidu_no_api.py "关键词" [-n 数量] [-o 输出文件]

输出: JSON 到 stdout，包含标题、链接、摘要。

依赖: requests, lxml (已预装)
"""

import sys
import json
import random
import argparse
from urllib.parse import quote

import requests
from lxml import html

# ── User-Agent 池 (20 个) ──────────────────────────────────────────
USER_AGENTS = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edg/123.0.0.0 Chrome/123.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edg/122.0.0.0 Chrome/122.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:123.0) Gecko/20100101 Firefox/123.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 16_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPad; CPU OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; Mi 11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36',
]

BASE_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'identity',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

# ── 辅助函数 ────────────────────────────────────────────────────────

def random_ua() -> str:
    """随机返回一个 User-Agent"""
    return random.choice(USER_AGENTS)


def build_session() -> requests.Session:
    """创建带随机 UA 的 requests Session"""
    s = requests.Session()
    s.headers.update(BASE_HEADERS)
    s.headers['User-Agent'] = random_ua()
    return s


def search_page(query: str, timeout: int = 15) -> str:
    """
    搜索 www.baidu.com，返回 HTML 文本。
    """
    encoded = quote(query)
    url = f'https://www.baidu.com/s?wd={encoded}'

    headers = dict(BASE_HEADERS)
    headers['User-Agent'] = random_ua()
    headers['Host'] = 'www.baidu.com'
    headers['Referer'] = 'https://www.baidu.com/'

    resp = requests.get(url, headers=headers, timeout=timeout)
    resp.encoding = 'utf-8'
    return resp.text


def parse_results(html_text: str, max_results: int) -> list[dict]:
    """
    从百度搜索结果 HTML 中解析结果列表。
    """
    results = []
    try:
        tree = html.fromstring(html_text.encode('utf-8'))
    except Exception:
        return results

    # 百度搜索结果容器：div.result 和 div.c-container
    items = tree.xpath(
        "//div[contains(@class, 'result')] | "
        "//div[contains(@class, 'c-container')]"
    )

    for item in items:
        if len(results) >= max_results:
            break

        try:
            # 标题 & URL
            title_els = item.xpath(
                ".//h3//a//text() | "
                ".//a[contains(@class, 'c-title')]//text()"
            )
            title = ''.join(title_els).strip() if title_els else ''
            href_els = item.xpath(
                ".//h3//a/@href | "
                ".//a[contains(@class, 'c-title')]/@href"
            )
            href = href_els[0] if href_els else ''

            # 摘要
            summary_els = item.xpath(
                ".//div[contains(@class, 'c-abstract')]//text() | "
                ".//div[contains(@class, 'abstract')]//text() | "
                ".//span[contains(@class, 'content-right_')]//text()"
            )
            summary = ''.join(summary_els).strip() if summary_els else ''

            if title and href:
                results.append({
                    'title': title,
                    'url': href,
                    'summary': summary,
                })
        except Exception:
            continue

    return results


def search_baidu_no_api(query: str, max_results: int = 10, timeout: int = 15) -> dict:
    """
    搜索百度（无 API），返回 {"query": ..., "total": ..., "results": [...]}
    """
    max_results = min(max_results, 50)

    try:
        html_text = search_page(query, timeout=timeout)
        results = parse_results(html_text, max_results)
    except Exception as e:
        return {
            'query': query,
            'total': 0,
            'results': [],
            'error': str(e),
        }

    return {
        'query': query,
        'total': len(results),
        'results': results,
    }


# ── CLI 入口 ─────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='百度搜索 — 无需 API Key (www.baidu.com)'
                    ' — Baidu MCP 不可用时的兜底方案',
    )
    parser.add_argument('query', help='搜索关键词')
    parser.add_argument('-n', '--num', type=int, default=10,
                        help='返回结果数量 (默认 10，最大 50)')
    parser.add_argument('-o', '--output', type=str, default='',
                        help='输出 JSON 文件路径 (可选)')
    args = parser.parse_args()

    try:
        print(f'[Baidu no-API] 正在搜索: "{args.query}"...', file=sys.stderr)
        result = search_baidu_no_api(args.query, max_results=args.num)

        json_output = json.dumps(result, ensure_ascii=False, indent=2)

        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(json_output)
            print(f'[Baidu no-API] 结果已保存到: {args.output}', file=sys.stderr)

        print(json_output)

    except Exception as e:
        error_result = {
            'query': args.query,
            'total': 0,
            'results': [],
            'error': str(e),
        }
        print(json.dumps(error_result, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == '__main__':
    main()
