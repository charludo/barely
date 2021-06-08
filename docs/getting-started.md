# Getting Started

Good news: Getting started with barely is super easy! This guide elaborates on the [Quickstart Guide](/README.md#quickstart) in the README.

## Prerequisites

Make sure you have python >= 3.9 installed:
```console
$ python -V
Python 3.9.x
```

If you prefer, create a virtual environment for barely:
```console
$ python -m venv .venv
$ . .venv/bin/activate
(.venv) $
```

## Installation

Now, simply install barely like any other package:
```console
(.venv) $ pip install barely
```

That's it! Congrats!

<!-- USAGE -->
## Usage Basics

Now let's get familiar with using barely!

1. Type `barely --help` to get an overview over available commands and options:
	```console
	$ barely --help
	Usage: barely [OPTIONS] COMMAND [ARGS]...

	  barely reduces static website development to its key parts, by
	  automatically rendering jinja2 templates and Markdown content into HTML. A
	  simple plugin interface allows for easy extensibility, and the built-in
	  live web server makes on-the-fly development as comfortable as possible.

	Options:
	  --help  Show this message and exit.

	Commands:
	  blueprints  list all available blueprints, or create a new one
	  live        starts a live server, opens your project in the browser and...
	  new         create a new barely project (optionally with a blueprint)
	  rebuild     (re)build the entire project
	  test        run the testsuite to verify the install
	```

2. Try typing `barely`, `barely live`, or `barely rebuild`:
	```console
	$ barely
	barely :: could not find 'config.yaml'. Exiting
	```
	What happened? barely is telling us that we aren't currently in a barely project directory. For a directory to count as a project, it has to contain a `config.yaml` file, which in turn has to specify the devroot (where we will work) and the webroot (where barely renders to).

	So lets change that!

3. Create a new project with `barely new`:
	```console
	$ barely new
	barely :: setting up new project with parameters:
	       ->   webroot: webroot
	       ->   devroot: devroot
	       -> blueprint: default
	barely :: setting up basic config...
	barely :: done.
	```
	Sweet! barely created two new subdirectories, `devroot` and `webroot`. The project was also created with a blueprint, namely `default`, which is why our `devroot` is not empty. We will learn about blueprints in a second.

	BTW: you can easily change the project creation parameters, see for reference:
	```console
	$ barely new --help
	Usage: barely new [OPTIONS]

	 create a new barely project (optionally with a blueprint)

	Options:
	 -b, --blueprint TEXT  instantiate project from a blueprint
	 -w, --webroot TEXT    location for the generated static files
	 -d, --devroot TEXT    project directory, for development files
	 --help                Show this message and exit.
	```

4. Let's have a look around!
	```console
	$ cd devroot
	$ tree .
	.
	├── config.yaml
	├── metadata.yaml
	├── template.md
	└── templates
	    ├── template2.html
	    └── template.html

	1 directory, 5 files
	```
	- `config.yaml` contains all the configuration for barely and its plugins. Right now, it only contains the absolute paths of the devroot and webroot
	- `metadata.yaml` is a place you can put any values you want to use in multiple places across your project, be it metadata or any other variables
	- `template.md` is the Markdown file for the root page of the website. Its contents will get rendered into `webroot/index.html` with the `templates/template.md` template
	- `templates/` contains all your templates

6. Let's build the project!
	```console
	$ barely rebuild
	barely :: registering plugins...
	barely :: 8 plugins registered.
	barely :: starting full rebuild...
	       :: deleted /[...]/test/webroot
	barely :: event at /[...]/test/devroot/template.md
	       :: rendered, highlighted /[...]/template.md -> /[...]/webroot/index.html
	barely :: full rebuild complete.
	barely ..
	barely :: Do you want to Publish / Backup / do both?
	       -> [n]othing | [p]ublish | [b]ackup | *[Y]do both :: n
	barely :: exited.
	```

	And then start the live server:
	```console
	$ barely
	barely :: registering plugins...
	barely :: 8 plugins registered.
	barely :: started tracking...
	```

	Your favorite browser should open, and you will be greeted with the rendered version of `template.md`.

	Now is a good time to play around a bit with your sample project - make some changes to the contents, the templates or add a stylesheet and watch the page update in real time!

When you feel comfortable with the workings of barely, move on to the [next section](detailed-overview.md).

[< back](README.md)
