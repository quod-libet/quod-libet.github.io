#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Copyright 2016 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

import time
import urllib2
import feedparser
from multiprocessing.pool import ThreadPool

GITHUB = "https://github.com/quodlibet/quodlibet/releases/download/release-%(version)s/"

RELEASES = [
    "3.9.0 (2017-05-24)",
    "3.8.1 (2017-01-23)",
    "3.8.0 (2016-12-29)",
    "3.7.1 (2016-09-25)",
    "3.7.0 (2016-08-27)",
    "3.6.2 (2016-05-24)",
    "3.6.1 (2016-04-05)",
    "3.6.0 (2016-03-24)",
    "3.5.3 (2016-01-16)",
    "3.5.2 (2016-01-13)",
    "3.5.1 (2015-10-14)",
    "3.5.0 (2015-10-07)",
    "3.4.1 (2015-05-24)",
    "3.4.0 (2015-04-09)",
    "3.3.1 (2015-01-10)",
    "3.3.0 (2014-12-31)",
    "3.2.2 (2014-10-03)",
    "3.2.1 (2014-08-16)",
    "3.2.0 (2014-08-01)",
]


def release_link(version):
    return ("https://quodlibet.readthedocs.io/en/latest/"
            "changelog.html#release-%s" % version.replace(".", "-"))


def release_date(date):
    return time.strftime("%a, %d %b %Y %H:%M:%S +0000",
                         time.strptime(date, "%Y-%m-%d"))


BUILDS = {
    "osx-quodlibet": {
        "title": "Quod Libet (OS X)",
        "os": "",
        "releases": [
            ("3.9.0", "0", GITHUB + "QuodLibet-%(version)s.dmg"),
            ("3.8.1", "0", GITHUB + "QuodLibet-%(version)s.dmg"),
            ("3.8.0", "0", GITHUB + "QuodLibet-%(version)s.dmg"),
            ("3.7.1", "0", GITHUB + "QuodLibet-%(version)s.dmg"),
            ("3.7.0", "0", GITHUB + "QuodLibet-%(version)s.dmg"),
            ("3.6.1", "0", GITHUB + "QuodLibet-%(version)s.zip"),
            ("3.5.2", "1", GITHUB + "QuodLibet-%(version)s-v2.zip"),
            ("3.5.2", "0", GITHUB + "QuodLibet-%(version)s.zip"),
            ("3.5.1", "0", GITHUB + "QuodLibet-%(version)s.zip"),
            ("3.5.0", "1", GITHUB + "QuodLibet-%(version)s-v2.zip"),
            ("3.5.0", "0", GITHUB + "QuodLibet-%(version)s.zip"),
            ("3.4.1", "1", GITHUB + "QuodLibet-%(version)s.zip"),
            ("3.4.1", "0", GITHUB + "QuodLibet-%(version)s.zip"),
        ],
    },
    "osx-exfalso": {
        "title": "Ex Falso (OS X)",
        "os": "",
        "releases": [
            ("3.9.0", "0", GITHUB + "ExFalso-%(version)s.dmg"),
            ("3.8.1", "0", GITHUB + "ExFalso-%(version)s.dmg"),
            ("3.8.0", "0", GITHUB + "ExFalso-%(version)s.dmg"),
            ("3.7.1", "0", GITHUB + "ExFalso-%(version)s.dmg"),
            ("3.7.0", "0", GITHUB + "ExFalso-%(version)s.dmg"),
            ("3.6.1", "0", GITHUB + "ExFalso-%(version)s.zip"),
            ("3.5.2", "1", GITHUB + "ExFalso-%(version)s-v2.zip"),
            ("3.5.2", "0", GITHUB + "ExFalso-%(version)s.zip"),
            ("3.5.1", "0", GITHUB + "ExFalso-%(version)s.zip"),
            ("3.5.0", "1", GITHUB + "ExFalso-%(version)s-v2.zip"),
            ("3.5.0", "0", GITHUB + "ExFalso-%(version)s.zip"),
            ("3.4.1", "1", GITHUB + "ExFalso-%(version)s.zip"),
            ("3.4.1", "0", GITHUB + "ExFalso-%(version)s.zip"),
        ],
    },
    "windows": {
        "title": "Quod Libet / Ex Falso (Windows)",
        "os": "windows",
        "releases": [
            ("3.9.0", "0", GITHUB + "quodlibet-%(version)s-installer.exe"),
            ("3.8.1", "0", GITHUB + "quodlibet-%(version)s-installer.exe"),
            ("3.8.0", "0", GITHUB + "quodlibet-%(version)s-installer.exe"),
            ("3.7.1", "0", GITHUB + "quodlibet-%(version)s-installer.exe"),
            ("3.7.0", "0", GITHUB + "quodlibet-%(version)s-installer.exe"),
            ("3.6.1", "0", GITHUB + "quodlibet-%(version)s-installer.exe"),
            ("3.6.0", "0", GITHUB + "quodlibet-%(version)s-installer.exe"),
            ("3.5.2", "0", GITHUB + "quodlibet-%(version)s-installer.exe"),
            ("3.5.1", "0", GITHUB + "quodlibet-%(version)s-installer.exe"),
            ("3.5.0", "0", GITHUB + "quodlibet-%(version)s-installer.exe"),
            ("3.4.1", "0", GITHUB + "quodlibet-%(version)s-installer.exe"),
        ],
    },
    "windows-portable": {
        "title": "Quod Libet / Ex Falso (Windows Portable)",
        "os": "windows",
        "releases": [
            ("3.9.0", "0", GITHUB + "quodlibet-%(version)s-portable.exe"),
            ("3.8.1", "0", GITHUB + "quodlibet-%(version)s-portable.exe"),
            ("3.8.0", "0", GITHUB + "quodlibet-%(version)s-portable.exe"),
            ("3.7.1", "0", GITHUB + "quodlibet-%(version)s-portable.exe"),
            ("3.7.0", "0", GITHUB + "quodlibet-%(version)s-portable.exe"),
            ("3.6.1", "0", GITHUB + "quodlibet-%(version)s-portable.exe"),
            ("3.6.0", "0", GITHUB + "quodlibet-%(version)s-portable.exe"),
            ("3.5.2", "0", GITHUB + "quodlibet-%(version)s-portable.exe"),
            ("3.5.1", "0", GITHUB + "quodlibet-%(version)s-portable.exe"),
            ("3.5.0", "0", GITHUB + "quodlibet-%(version)s-portable.exe"),
            ("3.4.1", "0", GITHUB + "quodlibet-%(version)s-portable.exe"),
        ],
    },
    "default": {
        "title": "Quod Libet / Ex Falso",
        "os": "linux",
        "releases": [
            ("3.9.0", "0", GITHUB + "quodlibet-%(version)s.tar.gz"),
            ("3.8.1", "0", GITHUB + "quodlibet-%(version)s.tar.gz"),
            ("3.8.0", "0", GITHUB + "quodlibet-%(version)s.tar.gz"),
            ("3.7.1", "0", GITHUB + "quodlibet-%(version)s.tar.gz"),
            ("3.7.0", "0", GITHUB + "quodlibet-%(version)s.tar.gz"),
            ("3.6.2", "0", GITHUB + "quodlibet-%(version)s.tar.gz"),
            ("3.6.1", "0", GITHUB + "quodlibet-%(version)s.tar.gz"),
            ("3.6.0", "0", GITHUB + "quodlibet-%(version)s.tar.gz"),
            ("3.5.2", "0", GITHUB + "quodlibet-%(version)s.tar.gz"),
            ("3.5.1", "0", GITHUB + "quodlibet-%(version)s.tar.gz"),
            ("3.5.0", "0", GITHUB + "quodlibet-%(version)s.tar.gz"),
            ("3.4.1", "0", GITHUB + "quodlibet-%(version)s.tar.gz"),
        ],
    },
}

TEMPLATE = """\
<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0" \
xmlns:sparkle="http://www.andymatuschak.org/xml-namespaces/sparkle" \
xmlns:dc="http://purl.org/dc/elements/1.1/">
  <channel>
    <title>%(title)s</title>
    <link>%(link)s</link>
%(items)s\
</channel>
</rss>
"""

ITEM = """\
    <item>
      <title>Version %(version_desc)s</title>
      <sparkle:releaseNotesLink>
        %(changelog)s
      </sparkle:releaseNotesLink>
      <link>%(changelog)s</link>
      <pubDate>%(date)s</pubDate>
      <enclosure url="%(url)s" %(os)s sparkle:version="%(version_key)s" \
length="%(length)s" type="application/octet-stream" />
    </item>
"""


def get_size(url):
    try:
        r = urllib2.urlopen(url)
        length = r.info().get("Content-Length", "0")
        r.close()
    except:
        print url
        raise
    return url, length


def main():
    release_dates = {}
    for r in RELEASES:
        version, date = r.split()
        date = release_date(date.strip("()"))
        release_dates[version] = date

    url_lengths = {}
    for t in BUILDS.values():
        for r in t["releases"]:
            url_lengths[r[-1] % {"version": r[0]}] = ""

    pool = ThreadPool(20)
    for url, length in pool.imap_unordered(get_size, url_lengths):
        url_lengths[url] = length
    pool.close()
    pool.join()

    for type_id, type_ in BUILDS.items():
        items = []
        title = type_["title"]
        os_ = type_["os"]
        for version, build, url in type_["releases"]:
            print type_id, version
            url = url % {"version": version}
            if url in url_lengths:
                length = url_lengths[url]
            else:
                length = "0"
            version_desc = version
            version_key = version
            if build != "0":
                version_desc += " (v%d)" % (int(build) + 1, )
                version_key += "." + build
            date = release_dates[version]
            item = ITEM % {
                "version_desc": version_desc,
                "version_key": version_key,
                "length": length,
                "url": url,
                "date": date,
                "changelog": release_link(version),
                "os": ("sparkle:os=\"%s\"" % os_) if os_ else "",
            }
            items.append(item)

        result = TEMPLATE % {
            "title": title,
            "link": "https://quodlibet.readthedocs.io/en/latest/downloads.html",
            "items": "".join(items),
        }

        path = type_id + ".rss"
        with open(path, "wb") as h:
            h.write(result)
        feedparser.parse(path)

if __name__ == "__main__":
    main()
