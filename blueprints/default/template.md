---
title: Hi barely!
---

# Welcome to barely

<!-- ABOUT -->
## About barely

barely was built out of frustration with the readily available site generators, frameworks and CMS, which mostly fall into two categories: not providing crucial features; or providing such an overload of them that gettig started with the system takes longer than just building the site by hand.

barely reduces static website development to its key parts, by automatically rendering jinja2 templates and Markdown content into HTML. A simple **plugin interface** allows for easy extensibility, and the built-in **live web server** makes on-the-fly development as comfortable as possible.

For more on barelys design philosophy, and to see whether barely might be right for your project, [see here in the docs](docs/about.md).



<!-- Quickstart -->
## Quickstart

Good news: Getting started with barely is super easy! So we will keep this quick. For more info on Getting Started, [see this page in the docs](docs/getting-started.md).

### Prerequisites

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

### Installation

Now, simply install barely like any other package:
```console
(.venv) $ pip install barely
```

That's it! Congrats!

<!-- USAGE EXAMPLES -->
## Usage

- [Basics](#basics)
- [Core Mechanics](#core-mechanics)
- [Modular Pages](#modular-pages)
- [Plugins](#plugins)
- [Blueprints](#blueprints)

### Basics

Now let's get familiar with using barely!

1. Create a new project with `barely new`:
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

2. Now let's build the project!
	```console
    $ cd devroot
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

	For a more thorough explanation, make sure to check out [Getting Started](docs/getting-started.md) in the docs!


### Core Mechanics

There are a couple of things that are important to know about how barely works. If you've used similar frameworks before, you'll probably already be familiar with most of these things. barely doesn't try to reinvent the wheel.

- the structure of your site is defined in jinja2 templates. By default, these are stored in the `templates/` folder
- you write the contents of your pages with [Markdown](https://guides.github.com/features/mastering-markdown/)
- each page can individually be configured using [YAML notation](docs/detailed-overview.md)
- global level configuration of barely happpens in the `config.yaml` file, global variables to be used in your templates are stored in `metadata.yaml`

This just scratches the surface; please, do yourself a favor and read the [Detailed Overview](docs/detailed-overview.md) in the docs.

### Modular Pages

Pages can be `modular`, meaning they contain subpages with their own contents and templates.
To define a modular page, simply put the "modular" argument into that pages configuration:
```yaml
---
title: My Parent Page
modular:
  - about
  - services
  - contact
---
```

To see how, when, and why to use them, see here: [Modular Pages](docs/modular-pages.md)

### Plugins

barely offers rather limited functionality on its own: "use some templates to render some contents into static HTML files". That's it.

But most of the time, you will want at least a little more functionality. That's where plugins come in!

barely comes with 10 plugins by default:

- [Collections](docs/plugins/collections.md)
- [Forms](docs/plugins/forms.md)
- [Highlight](docs/plugins/highlight.md)
- [Minimizer](docs/plugins/minimizer.md)
- [Reading Time](docs/plugins/readingtime.md)
- [Timestamps](docs/plugins/timestamps.md)
- [Table of Contents](docs/plugins/toc.md)
- [git](docs/plugins/git.md)
- [Local Backup](docs/plugins/localbackup.md)
- [SFTP](docs/plugins/sftp.md)

For more information on how to enable and configure a plugin, click on its respective name.

To learn how to install new plugins or write your own, see [the Plugins page](docs/plugins.md) in the docs.

### Blueprints

Back in the [Basics](#basics), we have already briefly covered blueprints. They are pretty much exactly what you would expect: re-usable project templates that you can instantiate into new projects. Other frameworks might call them themes.

You can list all available blueprints with:
```console
$ barely blueprints
barely :: found 2 blueprints:
	-> default
	-> blank
```

To learn how to create and use your own blueprints, see [Blueprints](docs/blueprints.md) in the docs.

<!-- ROADMAP -->
## Roadmap

barely is currently released as version `1.0.0`. That means that while everything works and the project is feature complete (in regards to its initial vision), there are still a lot of improvements to be made. Some important ones are:

- **better exception handling**. There are numerous ways to get an exception right now (for example: try renaming a page to a non-existent template) that really don't have to cause barely to exit.

- **better logging** - or really, *logging*. Currently, instead of a proper logger, barely just sometimes calls `print()`. Different levels of logging and some color are desperately needed.

- **performance improvements**. barely is fast enough for every-day use, but not exactly optimized. The biggest performance win could probably be made by letting barely interact with a model of the current project, instead of constantly opening / closing the same files. That's a major rework though, and maybe something for version 2.0.0...

- **the docs** could use some love :)

<!-- CONTRIBUTING -->
## Contributing

Contributors are highly appreciated! Check out [CONTRIBUTING.md](CONTRIBUTING.md) for more info!

**If you have written a plugin or created a blueprint and think others might benefit, please do create a pull request!**


## Built With & Inspired By

This project would not have been possible without a lot of amazing FOSS projects. Most notable are:
- [jinja2](https://jinja.palletsprojects.com/en/3.0.x/)
- [livereload](https://github.com/lepture/python-livereload)
- [mistune](https://github.com/lepture/mistune)
- [pyyaml](https://pyyaml.org/wiki/PyYAMLDocumentation)

barely simply stitches them togehter in an exciting manner.

The various inspirations for barely should also not stay concealed:
- [flask](https://flask.palletsprojects.com/en/2.0.x/) doesn't need an introduction
- [grav](https://getgrav.org) is probably the closest (spiritual) relative


<!-- LICENSE -->
## License

Distributed under the GNU General Public License. See [LICENSE](LICENSE) for more information.


<!-- CONTACT -->
## Contact

Charlotte Hartmann Paludo - [@smiletolerantly](https://t.me/smiletolerantly) - contact@charlotteharludo.com

Project Link: [https://github.com/charludo/barely](https://github.com/charludo/barely)
