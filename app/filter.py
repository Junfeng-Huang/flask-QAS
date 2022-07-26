"""
Jinja2过滤器
"""
import bleach


def html2text(h: str):
    return bleach.clean(h, strip=True)