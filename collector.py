import urlparse
import re

twitter = re.compile('^http://twitter.com/(#!/)?(?P<account>[a-zA-Z0-9_]{1,15})$')


def collect(urls):
	collection = {'twitter':{}}
	for url in urls :
		up = urlparse.urlparse(url)
		hostname = up.hostname

		if hostname == None:
			continue

		if hostname == 'www.facebook.com':
			pass
		elif hostname == 'twitter.com':
			m = twitter.match(url)

			if m:
				gs = m.groupdict()
				if 'account' in gs:
					if gs['account'] != 'share': # this is not an account, although http://twitter.com/#!/share says that this account is suspended.
						collection['twitter'][gs['account']] = url
		elif hostname == 'www.linkedin.com':
			pass
		elif hostname == 'plus.google.com':
			pass
		elif hostname == 'www.slideshare.net':
			pass
		elif hostname == 'www.youtube.com':
			pass
		elif hostname == 'www.flickr.com':
			pass
		elif hostname[-9:] == '.xing.com':
			pass
		else:
			continue

#		collection.append(up.hostname)
	
	return collection

