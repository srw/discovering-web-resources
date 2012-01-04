import lxml.html
import urlparse

def get_all_links(page, base = ''):
	doc = lxml.html.fromstring(page)
	links = map(lambda x: urlparse.urljoin(base, x.attrib['href']), filter(lambda x: 'href' in x.attrib, doc.xpath('//a')))

	return links

def get_all_feeds(page, base = ''):
	doc = lxml.html.fromstring(page)

	feeds = map(lambda x: {'href':urlparse.urljoin(base, x.attrib['href']),'type':x.attrib['type']}, filter(lambda x: 'type' in x.attrib and x.attrib['type'] in ['application/atom+xml', 'application/rss+xml'], doc.xpath('//link')))

	return feeds


