# coding: utf-8
from __future__ import unicode_literals

import string
import random
import time
import re

from .common import InfoExtractor


class DoodStreamIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?dood\.(?:to|watch|so|re|wf)/[ed]/(?P<id>[a-z0-9]+)'
    _TEST = {
        'url': 'https://dood.to/d/9di5z1vfnwqe',
        'md5': 'a8dcc12df73eeedf86206f665fc51100',
        'info_dict': {
            'id': '9di5z1vfnwqe',
            'ext': 'mp4',
            'title': "Hijab mulus - DoodStream",
            'description': None,
            'thumbnail': 'https://img.doodcdn.co/splash/1z5fk5htzw3a9ei2.jpg',
        }
    }

    @staticmethod
    def _extract_urls(webpage):
        return re.findall(
            r'<iframe[^>]+?src=["\'](?P<url>(?:https?://)?dood\.(?:watch|to|so|re|wf)/e/.+?)["\']',
            webpage)

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)

        if '/d/' in url:
            url = "https://dood.to" + self._html_search_regex(
                r'<iframe src="(/e/[a-z0-9]+)"', webpage, 'embed')
            video_id = self._match_id(url)
            webpage = self._download_webpage(url, video_id)

        # title = self._html_search_meta(['og:title'],
        #                                webpage, default=None)
        title = self._html_search_regex(r'<title>(.+?)</title>',webpage,'title')
        print(title)
        thumb = self._html_search_meta(['og:image', 'twitter:image'],
                                       webpage, default=None)
        token = self._html_search_regex(r'[?&]token=([a-z0-9]+)[&\']', webpage, 'token')
        description = self._html_search_meta(
            ['og:description', 'description', 'twitter:description'],
            webpage, default=None)
        auth_url = 'https://dood.to' + self._html_search_regex(
            r'(/pass_md5.*?)\'', webpage, 'pass_md5')
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/66.0',
            'referer': url
        }

        webpage = self._download_webpage(auth_url, video_id, headers=headers)
        final_url = webpage + ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(10)]) + "?token=" + token + "&expiry=" + str(int(time.time() * 1000))

        return {
            'id': video_id,
            'title': title,
            'url': final_url,
            'http_headers': headers,
            'ext': 'mp4',
            'description': description,
            'thumbnail': thumb,
        }
