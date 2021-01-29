
def setPageActive(context, page_name):
  index = -1
  for n, page in enumerate(context['sidebar_pages']):
      if page['name'] == page_name:
          index = n
          break

  if index > -1:
    context['sidebar_pages'][index]['active'] = True
  
  return context
