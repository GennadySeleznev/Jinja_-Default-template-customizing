"""
useful context filters, see
http://jinja.pocoo.org/docs/dev/api/#jinja2.contextfilter
"""
import jinja2


@jinja2.contextfilter
def reverse_url(context, name_, **parts):
    """Filter for generating urls.

    See http://aiohttp.readthedocs.io/en/stable/web.html#
    reverse-url-constructing-using-named-resources

    Usage:

      {{ 'the-view-name'|url }} might become "/path/to/view"

    or with parts and a query

      {{ 'item-details'|url(id=123, query={'active': 'true'}) }} might 
      become "/items/1?active=true

    :param context: jinja2 context
    :param name_: the name of the route
    :param parts: url parts to be passed to route.url(), if parts 
        includes "query" it's removed and passed separately
    :return: url as generated by 
        app.route[<name>].url(parts=parts, query=query)
    """
    app = context['app']
    kwargs = {}
    if 'query' in parts:
        kwargs['query'] = parts.pop('query')
    if parts:
        kwargs['parts'] = parts
    return app.router[name_].url(**kwargs)


@jinja2.contextfilter
def static_url(context, static_file_path):
    """Filter for generating urls for static files.
    
    NOTE: you'll need to set app['static_root_url'] to be used as
     the root for the urls returned. 

    Usage:

      {{ 'styles.css'|static }} might become 
        "/static/styles.css" or "http://mycdn.example.com/styles.css"

    :param context: jinja2 context
    :param static_file_path: path to static file under static route
    :return: roughly just "<static_root_url>/<static_file_path>"
    """
    app = context['app']
    try:
        static_url = app['static_root_url']
    except KeyError:
        raise RuntimeError(
            "app does not define a static root url 'static_root_url', "
            "you need to set the url root with "
            "`app['static_root_url'] = '<static root>'`."
        )
    return '{static_url}/{file_path}'.format(
        static_url=static_url.rstrip('/'),
        file_path=static_file_path.lstrip('/'),
    )


DEFAULT_FILTERS = dict(
    url=reverse_url,
    static=static_url,
)
