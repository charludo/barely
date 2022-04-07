---
title: Building a blog with barely
summary: "Building a blog upon the foundations of a static site generator might appear to be counterintuitive. After all, aren't frequent updates the point, and blogs therefore inherently dynamic? But alas: we can have our cake and eat it, too!"
gitalong: barely/tree/main/barely/blueprints/blog
collections:
  - barely
  - python
  - all
  - featured
created: 2022-04-01
---
## Introduction

In this blog post, we are going to build a blog. Or rather, we are going to build *this* blog. (I know, a fitting topic for the first post on here, isn't it?) Rather than build it by hand or with the help of a bulky CMS however, we are going to use the static site generator [barely](https://buildwithbarely.org).

Apart from a slew of quality of life features (like hot reloading, SASS compilation and automatic .webp conversion), barely also offers us everything we need to build a blog "out of the box", most importantly a collection system to organize our posts into categories and link them appropriately.

## Setting up barely

First, let's install barely inside a Python virtual environment, create a new project and build it.
```console
$ python -m venv .venv
$ . .venv/bin/activate
$ pip install barely
$ barely new
$ cd devroot
$ barely rebuild -s
```

Your favorite browser should open and greet you with the rendered version of the project. Any changes you make from now on will immediately be reflected in the browser.

If we have a look in the `config.yaml` file, we can see that right now, it only contains information on where our project lives:
```yaml
ROOT:
  DEV: "/path/to/devroot"
  WEB: "/path/to/webroot"
```

We will gradually be extending this file with the configuration of a number of the plugins barely ships with. Let us start simple, however: with a "Hello World!" blog post.

## Building the blog

In the `templates` directory, create a new file `post.html`. Here, we define the structure of our blog posts. Initially, all we want is to display the title of the post and its content:
```html
{% extends "partials/base.html" %}

{% block body %}
<div class="blogpost">
	<h1>{{ title }}</h1>
	<div class="postbody">
		{{ content }}
	</div>
</div>
{% endblock %}
```

The first line simply states that we'd like to extend the (already existing) `base.html` template, so we won't have to worry about including stylesheets, adding `<meta>` tags, or building a menu in this file. Instead, all we care about is the content of the page, which is wrapped in a jinja block called body.

To utilize this template, create a new file `/blog/hello-world/post.md`, and paste the following into it:
```markdown
---
title: Hello World!
---

This is the content of our "Hello World" post!
```

If you are unclear on how the yaml configuration at the top of the file works, check out [this introduction](https://buildwithbarely.org/features/yaml/). To see your post, navigate to [http://127.0.0.1:5500/blog/hello-world/](http://127.0.0.1:5500/blog/hello-world/).

Alright, a title and some content are good, but not exactly a fully featured blog yet. So let's take it from the top.

### Timestamps
A common feature in blogs are created on / edited on timestamps. These are helpful to your readers to allow them to quickly gauge whether a post is still relevant to them ("The hottest Windows tips & tricks - written 1999-12-01" is probably not what they are looking for in 2022, for example...)

An easy way to convey this information is to add a `created` field below our title:
```yaml
title:  "Hello World!"
created: "2022-04-01"
```
which may then be displayed in the post template:
```html
...
<p>{{ created }}</p>
<h1>{{ title }}</h1>
...
```

However, an even easier way is to enable the Timestamps plugin included in barely, which provides created and edited timestamps. In your `config.yaml`, add:
```yaml
TIMESTAMPS:
  FORMAT: "%Y-%m-%d"
```

We would like to always display the created date, but only display the edited date if it diverges from the creation timestamp. Thankfully, jinja allows for conditional blocks:
```html
<p>{{ created }}{% if edited != created %} (edited: {{ edited }}){% endif %}</p>
```

Feel free to adjust the date format to your liking.

### Reading time
Similarly of interest to readers is an estimate of how long a given blog post is. Again, we could simply estimate this manually for every post. But the job of a static site generator is to make our lives easier! The ReadingTime plugin is enabled by default. All we need to do is include its field in the post template:
```html
<p>{{ created }}{% if edited != created %} (edited: {{ edited }}){% endif %}</p>
<p>{{ reading_time }} min</p>
```
This will print something like "4 - 7 min" above each post. The upper and lower words per minute estimates can be configured in `config.yaml`, should you so desire.

### Table of Contents
This one is not strictly necessary, but personally I really appreciate blogs which provide a table of contents. It allows me to quickly jump to the section I'm actually interested in.

With barely, the ToC plugin is enabled by default. All you need to do is place it within the `post.html` template:
```html
<strong>Table of Contents:</strong>
{{ toc }}
```

For our blog, I have decided to never use `<h1>` headings within the post body. This size is reserved for the title of the post. The ToC doesn't know this, so an unnecessary layer is currently being generated. Additionally, I'd like to use ordered (numbered) lists instead of unordered (bullet point) lists. Appending the config with
```yaml
TOC:
  LIST_ELEMENT: "ol"
  MIN_DEPTH: 2
```
has the desired effects.

### Collections
This is the most important feature of our blog, and the last one we will look at in depth. We want to associate categories or tags with our posts, and be able to quickly see all other posts in the same category. Ideally, this should happen automatically, without us having to edit several category pages every time a new post is published.

barely calls this feature *collections*. Pages can be part of any number of collections, and can exhibit any number of collections. Additionally, barely can generate a page for every collection listing all associated posts, as well as an overview page listing all collections.

It's easiest to understand when seen in action, so let's append our project configuration once more:
```yaml
COLLECTIONS:
  PAGE: "tags"
  COLLECTION_TEMPLATE: "tag.html"
  OVERVIEW_TEMPLATE: "overview.html"
  OVERVIEW_TITLE: "List of all tags"
  ORDER_KEY: "date"
  ORDER_REVERSE: true
```
Alright, what are saying here? First, we tell the plugin that the path to the category pages is `/tags/`. Each individual collection page should be rendered using the `tag.html` template, which looks like this:
```html
{% extends "partials/base.html" %}

{% block body %}
	<h1>Blogposts tagged with "{{ title }}"</h1>
	{% for collectible in collectibles %}
		<div class="postpreview">
			<p>{{ collectible["date"] }}</p>
			<p>{{ collectible["reading_time"] }} min</p>
			<h2><a href="{{ collectible['href'] }}">{{ collectible["title"] }}</a></h2>
			<p>{{ collectible["preview"] }}</p>
		</div>
	{% endfor %}
{% endblock %}
```

As we can see, we simply display the relevant data about each collectible, provided to us by the Collections plugin.

`OVERVIEW_TEMPLATE` simply is the template for the overview over all available tags, with a title of `OVERVIEW_TITLE`:
```html
{% extends "partials/base.html" %}

{% block body %}
	<h1>{{ title }}</h1>
	{% for collection in collections_list %}
		<a href="{{ collection['href'] }}">#{{ collection["name"] }} {{ [collection["size"]] }}</a>
	{% endfor %}
{% endblock %}
```

The last two options of the configuration, `ORDER_KEY` and `ORDER_REVERSE` allow us to tell barely how to sort collectibles within collection pages or exhibitions. Here, we chose to sort by date, in descending order.

If you rebuilt the project right now, you might notice that neither the overview page, nor any collection pages are being generated. That's because we haven't created any collections yet! How do we do that? Well, we simply tell barely "this post is part of that collection"!
```yaml
title:  "Hello World!"
created: "2022-04-01"
collections:
  - "collection1"
  - "collection2"
```

After saving, the changes won't immediately be available. That's because barely waits until shutting down to gather all collectibles, to make sure none is missed. Simply `Ctrl+C` in your console, then run `barely` again, and three new pages will have become available: `/tags/`, `/tags/collection1/`, and `/tags/collection2/`.

Neat!

### Other features
These were the most important blog-specific features. There's loads of other stuff you might want to add: automatic resizing of pictures, automatic SEO, lexing & highlighting of code snippets,...

These are not really blog specific however, and are covered in detail [here](https://buildwithbarely.org/features/)!

## Comments & Search
"Hold up!" you might say at this point. "There's something missing! What about comments, and search functionality?" And you'd be right - we have not implemented these yet. However, that's less of an issue with barely, and more an issue of the nature of static websites.

We can't do database lookups to return search results - there's no database. If you really wanted to, you could use a solution like [ElasticSearch](https://www.elastic.co/elasticsearch/) to pre-index your content and thus make it searchable in the browser.

For commenting, solutions exist as well. Most require you to include some JS snippet within your `post.html`, which then loads an external commenting system. To me, the disadvantages of commenting systems, not to mention the increased loading times, outweigh the benefits. I decided to simply link to GitHub discussions below my posts, since readers of this blog are likely to be technically inclined, and to already have a GitHub account anyway.

## Publishing your blog
There's multiple ways you can go about this. Option 1: run `barely rebuild`, then manually upload the result to your webserver. However, this will get annoying fast. Option 2: set up a very simple CD pipeline!

### Defer the build process to GitHub actions
Yeah, you heard right! GitHub actions can do the heavy lifting for you. Simply create a repository for your blog and push your existing files to it.

You want your blog to be built every time you push to the main branch. The necessary steps are:
- cloning your project
- installing barely
- modifying `config.yaml` to reflect the new `ROOT` dirs
- build the project
- push the result to a new branch

The following action does just that (though it could definitely be improved upon):
```yaml
name: build
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python 3.9
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    - name: Install barely
      run: |
        pip install --upgrade barely
    - name: edit config.yaml
      run: |
        mv config.yaml old.yaml
        echo -e "ROOT:\n  DEV: $(pwd)\n  WEB: $(dirname $(pwd))/webroot\n" > config.yaml
        echo "$(tail -n +4 old.yaml)" >> config.yaml
        cat config.yaml
        rm old.yaml
    - name: build project
      run: |
        yes "n" | barely rebuild

    - name: Push
      uses: s0/git-publish-subdir-action@develop
      env:
        REPO: self
        BRANCH: build
        FOLDER: ../webroot
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        MESSAGE: "Build: ({sha}) {msg}"
```

### Host the build with Cloudflare
While many static site hosting services exist, my personal favorite solution is [Cloudflare Pages](https://pages.cloudflare.com/). You simply login with GitHub, select your repository and branch, and... that's it. You're done. Optionally, you can configure a CNAME DNS record for a domain you own to point to your project, but Cloudflare does also provide you with a free .pages.dev subdomain.

The beauty of this solution is: you don't technically need to have barely installed anymore. Simply add a new blog post, push it to GitHub, and the action will build the project. Around one minute later, Cloudflare notices the changes and publishes them.

## The result
If you'd like to see what a resulting blog might look like, look no further than... here! This blog builds upon what you have just read, both in terms of the project structure, as well as the publishing and hosting methods.

Of course, there's a lot of stuff we have not talked about: menus and footers, the home page, the RSS feed and CSS styling come to mind. These are not really blog-specific, however. If you'd still like to play around with the finished product, you luckily don't need to look further than barely itself: Starting with version 1.1.4, this blog comes bundled as a blueprint.

Try it out yourself!
```console
$ barely new --blueprint blog
```
