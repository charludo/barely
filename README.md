[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/charludo/barely">
    <img src="docs/images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">barely</h3>

  <p align="center">
    barely is a lightweight, but highly extensible static site generator.
    <br />
    <a href="https://github.com/charludo/barely/docs/README.md"><strong>Explore the docs »</strong></a>
    <br />
    <br />
	<a href="#plugins">See available Plugins</a>
	.
    <a href="#quickstart">Quickstart</a>
    ·
    <a href="https://github.com/charludo/barely/issues">Report Bug</a>
    ·
    <a href="https://github.com/charludo/barely/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-barely">About barely</a></li>
    <li>
      <a href="#quickstart">Quickstart</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a>
		<ul>
			<li><a href="#basics">Basics</a></li>
			<li><a href="#core-mechanics">Core Mechanics</a></li>
			<li><a href="#plugins">Plugins</a></li>
			<li><a href="#blueprints">Blueprints</a></li>
		</ul>
	</li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
	<li><a href="#build-with--inspired-by">Build with & Inspired By</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT -->
## About barely

barely was built out of frustration with the readily available site generators, frameworks and CMS, which mostly fall into two categories: not providing crucial features; or providing such an overload of them that gettig started with it takes longer than just building the site by hand.

barely reduces static website development to its key parts, by automatically rendering jinja2 templates and Markdown content into HTML. A simple plugin interface allows for easy extensibility, and the built-in live web server makes on-the-fly development as comfortable as possible.

For mor on barely's design philosophy, and to see whether barely might be right for your project, [see here in the docs](docs/about.md).



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

<ul>
	<li><a href="#basics">Basics</a></li>
	<li><a href="#core-mechanics">Core Mechanics</a></li>
	<li><a href="#plugins">Plugins</a></li>
	<li><a href="#blueprints">Blueprints</a></li>
</ul>

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
	Sweet! barely created two new subdirs, `devroot` and `webroot`. The project was also created with a blueprint, namely `default`, which is why our `devroot` is not empty. We will learn about blueprints in a second.

2. Let's build the project!
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

	And then let's start the live server:
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

There are a couple of things that are important to know. If you've used similar frameworks before, you'll probably already be familiar with most of them. barely doesn't try to reinvent the wheel.

- the structure of your sites is defined in jinja2 templates. By default, these are stored in the `templates/` folder
- you write the contents of your pages with [Markdown](https://guides.github.com/features/mastering-markdown/)
- each page can individually be configured using [YAML notation](docs/detailed-overview)
- global level configuation of barely happpens in the `config.yaml` file, global variables to be used in your templates are stored in `metadata.yaml`

This just scratches the surface; please, do yourself a favor and read the [Detailed Overview](docs/detailed-overview) in the docs.

### Plugins

barely offers rather limited functionality on its own: use some templates to render some contents into static HTML files.

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

For more info on how to enable and configure a plugin, click on its respective name.

To learn how to install new plugins or right your own, see [the Plugins page](docs/plugins.md) in the docs.

### Blueprints

Back in the [Basics](#basics), we have already briefly covered blueprints. They are pretty much exactly what you would expect: re-usable projects that you can instantiate into new projects.

You can list available blueprint with:
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

- **better exception handling**. There are numerous ways to get an exception right now (for example: try renaming a page to a non-existant template) that really don't have to cause barely to exit.

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

Distributed under the GNU General Public License. See `LICENSE` for more information.


<!-- CONTACT -->
## Contact

Charlotte Hartmann Paludo - [@smiletolerantly](https://t.me/smiletolerantly) - contact@charlotteharludo.com

Project Link: [https://github.com/charludo/barely](https://github.com/charludo/barely)


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/charludo/barely.svg?style=for-the-badge
[contributors-url]: https://github.com/charludo/barely/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/charludo/barely.svg?style=for-the-badge
[forks-url]: https://github.com/charludo/barely/network/members
[stars-shield]: https://img.shields.io/github/stars/charludo/barely.svg?style=for-the-badge
[stars-url]: https://github.com/charludo/barely/stargazers
[issues-shield]: https://img.shields.io/github/issues/charludo/barely.svg?style=for-the-badge
[issues-url]: https://github.com/charludo/barely/issues
[license-shield]: https://img.shields.io/github/license/charludo/barely.svg?style=for-the-badge
[license-url]: https://github.com/charludo/barely/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png
