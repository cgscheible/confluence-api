#!/usr/bin/env python3

import json
from markdownify import markdownify as md
from atlassian import Confluence

# TODO: externalize configs with getenv
# TODO: refactor into functions:
#       - get_pagecount
#       - get_all_pages
#       - save_page_as_markdown
#       - call processor API (dummy call)
#       - cleanup

confluence = Confluence(
    url='https://127.0.0.1:8443/confluence',
    username='admin',
    password='',
    verify_ssl = False )

space = 'CMDB'
title = 'DEMO0'

if not confluence.page_exists(space, title, type=None): 
  status = confluence.create_page(space=space,title=title, body='This is the body. You can use <strong>HTML tags</strong>!')
  print(status)


# Get results from cql search result with all related fields
cql = "(type=page and Space=" + space + ")"
cql_response = confluence.cql(cql, start=0, limit=None, expand=None, include_archived_spaces=None, excerpt=None)
#print("Total pagecount in space %s : %s" % (space, cql_response['totalSize']))

start = 0
limit = 100
pagecount = cql_response['totalSize']

all_pages = []

while True:
  pages = confluence.get_all_pages_from_space(space, start=start, limit=limit, status=None, expand=None, content_type='page')
  all_pages = all_pages + pages
  #if len(pages) < limit:
  if start > pagecount:
      break
  start = start + limit

#print(all_pages)

# loop through the page IDs from all_pages and save each page to a file
for page in all_pages:
  print(page['id'])
  page_id = page['id']
  filename = page['id'] + ".md"
  f = open(filename, 'w', encoding="utf-8")
  #contents = confluence.get_page_by_id(page_id, expand=None, status=None, version="Latest")
  contents = confluence.get_page_by_id(page_id, expand='body.storage')
  body_html = contents['body']['storage']['value']
  body_markdown = md(body_html)
  f.write(body_markdown)
  f.close()

