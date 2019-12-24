def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    {%- if cookiecutter.backend != 'zodb' %}
    config.add_route('home', '/')
    {%- endif %}
