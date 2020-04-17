from urllib.parse import urlparse


def format_url(url):
    """将url转换成统一格式，以便进行比较"""
    parse = urlparse(url)
    tail = url.split(parse.netloc)[1].rstrip('/')       # 如果结尾有'/'则删除掉
    protocol = parse.scheme
    host = parse.netloc
    if protocol == '' or protocol == 'http':        # 统一协议名称
        protocol = 'https'
    return protocol + '://' + host + tail

