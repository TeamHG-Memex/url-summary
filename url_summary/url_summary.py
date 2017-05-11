from collections import defaultdict
import random
from uuid import uuid4
from six.moves.urllib.parse import (
    urlsplit, parse_qsl, ParseResult, urlunsplit, quote_plus)
from typing import Iterable


def get_summary(urls, top_items=20, top_urls=3, sample=True):
    # type: (Iterable[str], int, int) -> UrlSummaryResult
    """ Return a summary for given list or iterable of ``urls``.
    ``top_items`` (20 by default) controls how many top-level items to show,
    and ``top_urls`` (3 by default) sets the number of random urls to show
    for each top-level item.
    Returns a UrlSummaryResult: a list subclass that has a nice
    Jupyter Notebook display.
    """
    index = defaultdict(list)
    value_index = defaultdict(set)
    for url in urls:
        index['all', ''].append(url)
        parsed = urlsplit(url)  # type: ParseResult
        index['netloc', format(parsed.netloc)].append(url)
        path = parsed.path.rstrip('/').split('/')
        for i in range(1, len(path)):
            index['path start', '/'.join(path[: i + 1])].append(url)
        for k, v in _parse_qsl(parsed.query or ''):
            index['query key', '?{}'.format(k)].append(url)
            value_index[k].add(v)
            index['query key=value', '?{}={}'.format(k, v)].append(url)
    items = sorted(index.items(), key=lambda x: (-len(x[1]), x[0]))
    summary = []
    for k, v in items[:top_items]:
        stat = {'len': len(v), 'sample': sorted(_sample(v, top_urls, sample=sample))}
        if k[0] == 'query key':
            stat['len_v_set'] = len(value_index.get(k[1][1:]))
        summary.append((k, stat))
    return UrlSummaryResult(summary)


def _sample(lst, n, seed=42, sample=True):
    if len(lst) <= n:
        return lst
    elif sample:
        random.seed(seed)
        return random.sample(lst, n)
    else:
        return lst[:n]


def _quote(s):
    return quote_plus(s, safe='/')


def _parse_qsl(s):
    return parse_qsl(s, keep_blank_values=True)


def _bold(x, bold=True):
    return '<b style="color: black">{}</b>'.format(x) if bold else x


def _urlencode_quoted(x):
    return '&'.join('{}={}'.format(k, v) for k, v in x)


class UrlSummaryResult(list):
    def _repr_html_(self):
        return '<ul>{}</ul>'.format(
            '\n'.join(self._render_sample(field, value, stat)
                      for (field, value), stat in self))

    def _render_sample(self, field, value, stat):
        el_id = uuid4()
        # Using "hidden" class defined by the Jupyter notebook
        sample_elements = [self._render_url(url, field, value) for url in stat['sample']]
        if stat['len'] > len(sample_elements):
            sample_elements.append('&hellip;')
        return '''\
        <li>
            <span href="#" style="cursor: pointer"
             onclick="\
                var el = document.getElementById('{id}'); \
                this.getElementsByTagName('SPAN')[0].textContent = \
                    el.classList.contains('hidden') ? '&#9660' : '&#9658'; \
                el.classList.toggle('hidden')"
             >{n:,} {field}: <b>{value}</b>{extra} <span>&#9658;</span></span>
            <ul id="{id}" class="hidden" style="margin-top: 0">{sample}</ul>
        </li>'''.format(
            id=el_id,
            n=stat['len'],
            field=field,
            value=value,
            extra=(' ({len_v_set:,} unique values)'.format(**stat)
                   if 'len_v_set' in stat else ''),
            sample='\n'.join('<li>{}</li>'.format(el) for el in sample_elements),
        )

    def _render_url(self, url, field, value):
        return '<a href="{href}" target="_blank">{url}</a>'.format(
            href=url, url=self._highlight(url, field, value))

    def _highlight(self, url, field, value):
        if field == 'all':
            return url
        parsed = urlsplit(url)  # type: ParseResult
        netloc = parsed.netloc
        path = parsed.path
        query = parsed.query
        if field == 'netloc':
            netloc = _bold(parsed.netloc)
        elif field == 'path start':
            s = len(value)
            path = '{}{}'.format(_bold(parsed.path[1:s]), parsed.path[s:])
        elif field == 'query key':
            key_value = value[1:]
            query = _urlencode_quoted(
                [(_bold(_quote(k), k == key_value), _quote(v))
                 for k, v in _parse_qsl(query)])
        elif field == 'query key=value':
            key_value, value_value = value[1:].split('=', 1)
            query = _urlencode_quoted(
                [(_bold(_quote(k), bold), _bold(_quote(v), bold))
                 for bold, k, v in (
                     (k == key_value and v == value_value, k, v)
                     for k, v in _parse_qsl(query))])
        return urlunsplit((parsed.scheme, netloc, path, query, parsed.fragment))
