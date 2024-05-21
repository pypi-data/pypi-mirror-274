

from xbot import web


def get_web_page_by_web_page(web_page):
    """根据网页对象获取网页对象"""
    product_name = getattr(
        web_page, "product_name",
        "cef" if web_page._controller == "CEFBrowser" else "firefox")
    return web.get_active(mode=product_name)


def get_web_page_product_name(web_page):
    """根据网页对象获取浏览器的名称"""
    product_name = getattr(
        web_page, "product_name",
        "cef" if web_page._controller == "CEFBrowser" else "firefox")
    return product_name
