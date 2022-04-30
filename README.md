# Archive of Our Own RSS

Suprisingly, AO3 doesn't support RSS for works
and I couldn't find an easy-to-understand solution,
so I made one myself.

## Install
```bash
poetry install
# For the lazy...
python3 main.py
# For the more upstanding
gunicorn 'ao3_rss:create_app()'
```
