
def setPageActive(context, page_name):
  for n, page in enumerate(context['sidebar_pages']):
      if page['link'][1:] == page_name:
        context['sidebar_pages'][n]['active'] = True
      else:
        context['sidebar_pages'][n]['active'] = False
  return context

def setPageActiveuser(context, page_name):
  for n, page in enumerate(context['sidebar_pages_user']):
      if page['link'][1:] == page_name:
        context['sidebar_pages_user'][n]['active'] = True
      else:
        context['sidebar_pages_user'][n]['active'] = False  
  return context

