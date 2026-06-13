#!/usr/bin/env python3
"""
搜狗微信公众号文章搜索 — 无需 API Key
通过搜狗微信搜索 (weixin.sogou.com) 获取微信公众号文章。

用法:
  python search_wechat.py "关键词" [-n 数量] [-o 输出文件]

输出: JSON 到 stdout，包含文章标题、链接、摘要、发布时间、公众号名称。

依赖: requests, lxml (已预装)
"""

import sys
import json
import time
import random
import re
import argparse
from datetime import datetime
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


def get_sogou_cookie(session: requests.Session) -> dict:
    """
    从搜狗视频页面获取 SNUID 等 Cookie。
    返回 {'SNUID': '...', 'cookie_str': '...'}
    """
    try:
        resp = session.get(
            'https://v.sogou.com/v?ie=utf8&query=&p=40030600',
            timeout=10,
        )
        cookies = session.cookies.get_dict()
        snuid = cookies.get('SNUID', '')
        cookie_parts = [f'{k}={v}' for k, v in cookies.items()]
        return {
            'SNUID': snuid,
            'cookie_str': '; '.join(cookie_parts),
        }
    except Exception:
        return {'SNUID': '', 'cookie_str': ''}


def search_page(session: requests.Session, query: str, page: int = 1,
                cookie_str: str = '', timeout: int = 15) -> str:
    """
    搜索单页，返回 HTML 文本。
    """
    encoded = quote(query)
    url = (
        f'https://weixin.sogou.com/weixin?query={encoded}'
        f'&s_from=input&_sug_=n&type=2&page={page}&ie=utf8'
    )
    headers = dict(BASE_HEADERS)
    headers['User-Agent'] = random_ua()
    headers['Host'] = 'weixin.sogou.com'
    headers['Referer'] = 'https://weixin.sogou.com/'
    if cookie_str:
        headers['Cookie'] = cookie_str

    resp = session.get(url, headers=headers, timeout=timeout)
    resp.encoding = 'utf-8'
    return resp.text


def parse_timestamp(script_text: str) -> str:
    """从 script 文本中提取 Unix 时间戳并格式化为 '%Y-%m-%d %H:%M:%S'"""
    match = re.search(r'(\d{10})', script_text)
    if match:
        ts = int(match.group(1))
        return datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    return ''


def parse_articles(html_text: str, max_results: int) -> list[dict]:
    """
    从搜狗微信搜索结果 HTML 中解析文章列表。
    """
    articles = []
    try:
        tree = html.fromstring(html_text.encode('utf-8'))
    except Exception:
        return articles

    items = tree.xpath("//ul[contains(@class,'news-list')]/li")
    if not items:
        return articles

    for item in items:
        if len(articles) >= max_results:
            break

        try:
            # 标题 & URL
            title_els = item.xpath(".//h3/a//text()")
            title = ''.join(title_els).strip() if title_els else ''
            href_els = item.xpath(".//h3/a/@href")
            href = href_els[0] if href_els else ''
            if href.startswith('/'):
                href = f'https://weixin.sogou.com{href}'

            # 摘要
            summary_els = item.xpath(".//p[contains(@class,'txt-info')]//text()")
            summary = ''.join(summary_els).strip() if summary_els else ''

            # 来源（公众号名称）
            source = ''
            source_els = item.xpath(".//span[contains(@class,'all-time-y2')]//text()")
            if source_els:
                source = ''.join(source_els).strip()
            if not source:
                account_els = item.xpath(".//a[contains(@class,'account')]//text()")
                if account_els:
                    source = ''.join(account_els).strip()

            # 发布时间
            pub_time = ''
            script_els = item.xpath(".//div[contains(@class,'s-p')]//script//text()")
            for s in script_els:
                t = parse_timestamp(s)
                if t:
                    pub_time = t
                    break

            if title and href:
                articles.append({
                    'title': title,
                    'url': href,
                    'summary': summary,
                    'source': source,
                    'published_at': pub_time,
                })
        except Exception:
            continue

    return articles


def search_wechat(query: str, max_results: int = 10, timeout: int = 15) -> dict:
    """
    搜索微信公众号文章，返回 {"query": ..., "total": ..., "articles": [...]}
    """
    max_results = min(max_results, 50)  # 最多 50 条
    session = build_session()

    # 获取 Cookie
    cookie_info = get_sogou_cookie(session)
    cookie_str = cookie_info.get('cookie_str', '')

    articles = []
    page = 1
    pages_needed = (max_results + 9) // 10  # 每页约 10 条

    while len(articles) < max_results and page <= pages_needed and page <= 5:
        try:
            html_text = search_page(session, query, page=page,
                                    cookie_str=cookie_str, timeout=timeout)

            remaining = max_results - len(articles)
            parsed = parse_articles(html_text, remaining)

            if not parsed:
                break  # 没有更多结果

            articles.extend(parsed)
            page += 1

            # 页间延迟 — 降低反爬风险
            if page <= pages_needed:
                time.sleep(0.5 + random.random() * 1.0)

        except Exception as e:
            # 遇到错误停止翻页，返回已获取的结果
            print(f'[WeChat] 第{page}页请求失败: {e}', file=sys.stderr)
            break

    return {
        'query': query,
        'total': len(articles[:max_results]),
        'articles': articles[:max_results],
    }


# ── CLI 入口 ─────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='搜狗微信公众号文章搜索 — 无需 API Key',
    )
    parser.add_argument('query', help='搜索关键词')
    parser.add_argument('-n', '--num', type=int, default=10,
                        help='返回结果数量 (默认 10，最大 50)')
    parser.add_argument('-o', '--output', type=str, default='',
                        help='输出 JSON 文件路径 (可选)')
    args = parser.parse_args()

    try:
        print(f'[WeChat] 正在搜索: "{args.query}"...', file=sys.stderr)
        result = search_wechat(args.query, max_results=args.num)

        json_output = json.dumps(result, ensure_ascii=False, indent=2)

        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(json_output)
            print(f'[WeChat] 结果已保存到: {args.output}', file=sys.stderr)

        # 主输出到 stdout — 供 Claude 读取
        print(json_output)

    except Exception as e:
        # 输出 JSON 错误格式，便于上层解析
        error_result = {
            'query': args.query,
            'total': 0,
            'articles': [],
            'error': str(e),
        }
        print(json.dumps(error_result, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == '__main__':
    main()
