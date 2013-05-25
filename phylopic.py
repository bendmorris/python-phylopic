#!/usr/bin/env python
import urllib
import urllib2
import json
import os
import sys

# find name id matches for a text string
name_search_url = 'http://phylopic.org/api/a/name/search?text=%s&options=icon'
# find images associated with a name id
image_search_url = 'http://phylopic.org/api/a/name/%s/images?subtaxa=true'
# thumbnail image from image id
thumbnail_url = 'http://phylopic.org/assets/images/submissions/%s.thumb.png'

def download_pics(*taxa, **kwargs):
    path = kwargs.get('path', '.')
    name = kwargs.get('name', None)
    max_images = kwargs.get('max_images', 3)

    for taxon in taxa:
        image_path = os.path.join(path, '%s.png' % taxon)
        if os.path.exists(image_path): continue
        print 'Downloading pic for %s...' % taxon,
        sys.stdout.flush()
        url = image_url(taxon, max_images=max_images)
        request = urllib2.urlopen(url)
        with open(image_path, 'wb') as image_file:
            while True:
                data = request.read(1024)
                if not data: break
                image_file.write(data)
        print 'done!'

def image_url(taxon, max_images=1):
    thumbnail_counts = {}
    for thumbnail in get_thumbnails(pic_search(taxon)):
        if not thumbnail in thumbnail_counts:
            thumbnail_counts[thumbnail] = 0
        thumbnail_counts[thumbnail] += 1
        if max_images and sum(thumbnail_counts.values()) > max_images: break

    thumbnails = sorted(thumbnail_counts.items(),
                        key = lambda (k,v): v,
                        reverse=True)
    if not thumbnails: raise Exception('No image found for taxon %s' % taxon)

    return thumbnails[0][0]

def pic_search(taxon):
    url = name_search_url % urllib.quote_plus(taxon)

    response = urllib2.urlopen(url)
    data = json.loads(response.read())
    response.close()
    
    assert data['success']

    for result in (name.get('icon',None) for name in data['result']):
        if result: result = result.get('uid', None)
        if result: yield result

def get_thumbnails(image_ids):
    for image_id in image_ids:
        yield thumbnail_url % image_id


if __name__ == '__main__':
    if len(sys.argv) > 1: taxa = sys.argv[1:]
    else:
        taxa = raw_input('Enter names of taxa, separated by commas: ')
        taxa = [x.strip() for x in taxa.split(',')]
    download_pics(*taxa)
