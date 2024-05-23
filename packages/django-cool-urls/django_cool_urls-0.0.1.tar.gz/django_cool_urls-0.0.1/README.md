![logo.png](docs/logo.png)

# Django Cool URLs

Tim Berners-Lee is credited with saying that "cool URLs don't change", but
sadly that's just not the case.  Cool URLs are changing all the time because
the people who run those sites are moving stuff around or just deleting
whole pages and domains.

If you have a long-running site full of links like a blog however, this means
that over time your site can be pointing to a lot of dead links, which is bad
for your SEO.  It's also annoying when you're looking over a post from 10 years
ago that says something like "[this](.) is some really nice work" and that link
404s.

With `django-cool-urls`, you can link to whatever you like and the state of
that page is captured from the moment you linked to it.  If the page ever
disappears from the web, you can automatically switch over to the local copy.

All you need to do is switch from doing this:

```html
<a href="https://something-awesome.ca/">Nifty!</a>
```

to this:

```html
<a href="{% cool_url 'https://something-awesome.ca/' %}">Nifty!</a>
```

If that page ever 404s, your site will switch to showing the locally cached
version.  Think of it like your own private [archive.org](https://archive.org/).

Currently, this project supports caching *most* pages (see the [Caveats](caveats.md) page)
as well as embedded video from YouTube, Vimeo, and Instagram.


* [Official documentation](https://danielquinn.gitlab.io/django-cool-urls/)
    * [Installation](https://danielquinn.gitlab.io/django-cool-urls/installation/)
    * [Configuration](https://danielquinn.gitlab.io/django-cool-urls/configuration/)
    * [How to use it](https://danielquinn.gitlab.io/django-cool-urls/how-to-use-it/)
    * [Caveats & troubleshooting](https://danielquinn.gitlab.io/django-cool-urls/caveats/)
    * [Development](https://danielquinn.gitlab.io/django-cool-urls/development/)
