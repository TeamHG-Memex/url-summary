import re

import url_summary


def test_get_summary():
    urls = [
        'http://example-one.com',
        'http://example.com',
        'http://example.com/foo',
        'http://example.com/foo/one',
        'http://example.com/foo/two',
        'http://example.com/foo/two?sort=asc',
        'http://example.com/foo/two?sort=asc&page=1',
        'http://example.com/foo/two?sort=asc&page=2',
        'http://example.com/foo/two?sort=asc&page=3',
        'http://example.com/foo/two?sort=desc&page=3',
        'http://example.com/foo/two?page',
        'http://example.com/foo/two?page=<blink>',
    ]
    assert list(url_summary.get_summary(urls, sample=False)) == [
        (('all', ''),
         {'len': 12,
          'sample': ['http://example-one.com',
                     'http://example.com',
                     'http://example.com/foo']}),
        (('netloc', 'example.com'),
         {'len': 11,
          'sample': ['http://example.com',
                     'http://example.com/foo',
                     'http://example.com/foo/one']}),
        (('path start', '/foo'),
         {'len': 10,
          'sample': ['http://example.com/foo',
                     'http://example.com/foo/one',
                     'http://example.com/foo/two']}),
        (('path start', '/foo/two'),
         {'len': 8,
          'sample': ['http://example.com/foo/two',
                     'http://example.com/foo/two?sort=asc',
                     'http://example.com/foo/two?sort=asc&page=1']}),
        (('query key', '?page'),
         {'len': 6,
          'len_v_set': 5,
          'sample': ['http://example.com/foo/two?sort=asc&page=1',
                     'http://example.com/foo/two?sort=asc&page=2',
                     'http://example.com/foo/two?sort=asc&page=3']}),
        (('query key', '?sort'),
         {'len': 5,
          'len_v_set': 2,
          'sample': ['http://example.com/foo/two?sort=asc',
                     'http://example.com/foo/two?sort=asc&page=1',
                     'http://example.com/foo/two?sort=asc&page=2']}),
        (('query key=value', '?sort=asc'),
         {'len': 4,
          'sample': ['http://example.com/foo/two?sort=asc',
                     'http://example.com/foo/two?sort=asc&page=1',
                     'http://example.com/foo/two?sort=asc&page=2']}),
        (('query key=value', '?page=3'),
         {'len': 2,
          'sample': ['http://example.com/foo/two?sort=asc&page=3',
                     'http://example.com/foo/two?sort=desc&page=3']}),
        (('netloc', 'example-one.com'),
         {'len': 1, 'sample': ['http://example-one.com']}),
        (('path start', '/foo/one'),
         {'len': 1, 'sample': ['http://example.com/foo/one']}),
        (('query key=value', '?page='),
         {'len': 1, 'sample': ['http://example.com/foo/two?page']}),
        (('query key=value', '?page=1'),
         {'len': 1, 'sample': ['http://example.com/foo/two?sort=asc&page=1']}),
        (('query key=value', '?page=2'),
         {'len': 1, 'sample': ['http://example.com/foo/two?sort=asc&page=2']}),
        (('query key=value', '?page=<blink>'),
         {'len': 1, 'sample': ['http://example.com/foo/two?page=<blink>']}),
        (('query key=value', '?sort=desc'),
         {'len': 1, 'sample': ['http://example.com/foo/two?sort=desc&page=3']})]

    url_summary.get_summary(urls)


def test_render():
    s = url_summary.get_summary(['http://example.com/foo/two?sort=asc'])

    def normalize(html):
        html = re.sub(r'id=".*?"', '', html)
        html = re.sub(r'onclick=".*?"', '', html)
        html = re.sub('\s+', ' ', html).strip()
        html = re.sub('>\s+', '>', html)
        html = re.sub('\s+>', '>', html)
        html = re.sub('>', '>\n', html).strip()
        return html

    assert (normalize('<a id="1" foo="bar">\n  text here</a>') ==
            '<a foo="bar">\ntext here</a>')

    print(normalize(s._repr_html_()))
    assert normalize(s._repr_html_()) == normalize('''
    <ul>
        <li>
            <span href="#" style="cursor: pointer">
                1 all: <b></b>
                <span>&#9658;</span>
            </span>
            <ul class="hidden" style="margin-top: 0">
                <li><a href="http://example.com/foo/two?sort=asc" target="_blank">
                    http://example.com/foo/two?sort=asc</a>
                </li>
            </ul>
        </li>
        <li>
            <span href="#" style="cursor: pointer">
                1 netloc: <b>example.com</b>
                <span>&#9658;</span>
            </span>
            <ul class="hidden" style="margin-top: 0">
                <li>
                    <a href="http://example.com/foo/two?sort=asc" target="_blank">
                        http://<b style="color: black">example.com</b>/foo/two?sort=asc</a>
                </li>
            </ul>
        </li>
        <li>
            <span href="#" style="cursor: pointer">
                1 path start: <b>/foo</b>
                <span>&#9658;</span>
            </span>
            <ul class="hidden" style="margin-top: 0">
                <li>
                    <a href="http://example.com/foo/two?sort=asc" target="_blank">
                        http://example.com/<b style="color: black">foo</b>/two?sort=asc</a>
                </li>
            </ul>
        </li>
        <li>
            <span href="#" style="cursor: pointer">
                1 path start: <b>/foo/two</b>
                <span>&#9658;</span>
            </span>
            <ul class="hidden" style="margin-top: 0">
                <li>
                    <a href="http://example.com/foo/two?sort=asc" target="_blank">
                        http://example.com/<b style="color: black">foo/two</b>?sort=asc</a>
                </li>
            </ul>
        </li>
        <li>
            <span href="#" style="cursor: pointer">
                1 query key: <b>?sort</b> (1 unique values)
                <span>&#9658;</span>
            </span>
            <ul class="hidden" style="margin-top: 0">
                <li>
                    <a href="http://example.com/foo/two?sort=asc" target="_blank">
                        http://example.com/foo/two?<b style="color: black">sort</b>=asc</a>
                </li>
            </ul>
        </li>
        <li>
            <span href="#" style="cursor: pointer">
                1 query key=value: <b>?sort=asc</b>
                <span>&#9658;</span>
            </span>
            <ul class="hidden" style="margin-top: 0">
                <li>
                    <a href="http://example.com/foo/two?sort=asc" target="_blank">
                        http://example.com/foo/two?<b style="color: black">sort</b>=<b style="color: black">asc</b>
                    </a>
                </li>
            </ul>
        </li>
    </ul>
    ''')
