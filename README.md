[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![PyPI - Downloads][pypi-shield]][pypi-url]
![PyPI](https://img.shields.io/pypi/v/barely)
[![Issues][issues-shield]][issues-url]
[![barely test](https://github.com/charludo/barely/actions/workflows/barely-test.yml/badge.svg?branch=main)](https://github.com/charludo/barely/actions/workflows/barely-test.yml)
![Lines of code](https://img.shields.io/tokei/lines/github/charludo/barely)
[![MIT License][license-shield]][license-url]
![Website](https://img.shields.io/website?down_color=red&down_message=down&up_color=success&up_message=online&url=https%3A%2F%2Fbuildwithbarely.org)


<br />
<p align="center">
  <a href="https://github.com/charludo/barely">
    <img src="https://raw.githubusercontent.com/charludo/barely/main/docs/logo.png" width="auto" height="100" alt="barely" >
  </a>



  <p align="center">
    barely is a lightweight, but highly extensible static site generator.
    <br />
    <a href="https://github.com/charludo/barely/blob/main/docs/README.md"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="#quickstart">Quickstart</a>
	·
    <a href="#plugins">See available Plugins</a>
    ·
    <a href="https://github.com/charludo/barely/issues">Report Bug</a>
    ·
    <a href="https://github.com/charludo/barely/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
1. [About barely](#about-barely)
2. [Quickstart](#quickstart)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
3. [Usage](#usage)
    - [Basics](#basics)
    - [Core Mechanics](#core-mechanics)
    - [Modular Pages](#modular-pages)
    - [Plugins](#plugins)
    - [Blueprints](#blueprints)
4. [Roadmap](#roadmap)
5. [Contributing](#contributing)
6. [Built with & Inspired by](#built-with--inspired-by)
7. [License](#license)
8. [Contact](#contact)
9. [Changelog](#changelog)


#### barely has a website now!
[see it here: buildwithbarely.org](https://buildwithbarely.org) - of course also built with barely!

## Demo

Short demo of barely's live reloading capabilities:

![barely live demo gif](https://raw.githubusercontent.com/charludo/barely/main/docs/barely-demo.gif)

<!-- ABOUT -->
## About barely

barely was built out of frustration with the readily available site generators, frameworks and CMS, which mostly fall into two categories: not providing crucial features; or providing such an overload of them that getting started with the system takes longer than just building the site by hand.

barely reduces static website development to its key parts, by automatically rendering jinja2 templates and Markdown content into HTML. A simple **plugin interface** allows for easy extensibility, and the built-in **live web server** makes on-the-fly development as comfortable as possible.

Since building performant and SEO-friendly websites is always important, barely comes bundled with a Google **Lighthouse** CLI option, letting you quickly generate reports about your sites health.

For more on barely's design philosophy, and to see whether barely might be right for your project, [see here in the docs](https://github.com/charludo/barely/blob/main/docs/about.md).



<!-- Quickstart -->
## Quickstart

Good news: Getting started with barely is super easy! So we will keep this quick. For more info on Getting Started, [see this page in the docs](https://github.com/charludo/barely/blob/main/docs/getting-started.md).

### Prerequisites

Make sure you have python >= 3.9 installed:
```console
$ python -V
Python 3.9.x
```

(On Windows: `py -V`)

It is highly recommended to create a virtual environment for barely, otherwise some parts may not work:
```console
$ python -m venv .venv
$ . .venv/bin/activate
(.venv) $
```

(On Windows: `py -m venv .venv` and `.venv\Scripts\activate`)

### Installation

Now, simply install barely like any other package:
```console
(.venv) $ pip install barely
```

(On Windows: `py -m pip install barely`)

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
    [barely][  core][ INFO] :: setting up new project with parameters:
                            ->   webroot: webroot
                            ->   devroot: devroot
                            -> blueprint: default
    [barely][  core][ INFO] :: setting up basic config...
    [barely][  core][ INFO] :: done.
	```
	Sweet! barely created two new subdirectories, `devroot` and `webroot`. The project was also created with a blueprint, namely `default`, which is why our `devroot` is not empty. We will learn about blueprints in a second.

2. Now let's build the project!
	```console
    $ cd devroot
	$ barely rebuild
    [barely][  core][ INFO] :: registering plugins...
    [barely][  core][ INFO] :: 7 plugins registered.
    [barely][  core][ INFO] :: rebuilding devroot...
                            -> deleted /[...]/webroot
    [barely][  core][ INFO] :: event at /[...]/devroot/template.md
                            -> rendered, highlighted /[...]/devroot/template.md -> /[...]/webroot/index.html
    [barely][  core][ INFO] :: rebuild complete.
    [barely][  core][ INFO] :: Finalizing plugin ReadingTime...
    [barely][  core][ INFO] :: Finalizing plugin ToC...
    [barely][  core][ INFO] :: Finalizing plugin AutoSEO...
    [barely][  core][ INFO] :: Finalizing plugin Highlight...
    [barely][  core][ INFO] :: Finalizing plugin Forms...
    [barely][  core][ INFO] :: Finalizing plugin Minify...
    [barely][  core][ INFO] :: Finalizing plugin Gallery...
    [barely][  core][ INFO] :: ..
                            -> Do you want to Publish / Backup / do both?
                            -> *[n]othing | [p]ublish | [b]ackup | [Y]do both :: n
    [barely][  core][ INFO] :: exited.
	```

	And then start the live server:
	```console
	$ barely
    [barely][  core][ INFO] :: registering plugins...
    [barely][  core][ INFO] :: 7 plugins registered.
    [barely][  core][ INFO] :: started tracking...
	```

	Your favorite browser should open, and you will be greeted with the rendered version of `template.md`.

    We could also have combined those two steps with the `-s` flag like this: `barely rebuild -s`, to start the live server immediately after rebuilding.

	Now is a good time to play around a bit with your sample project - make some changes to the contents, the templates or add a stylesheet and watch the page update in real time!

	For a more thorough explanation, make sure to check out [Getting Started](https://github.com/charludo/barely/blob/main/docs/getting-started.md) in the docs!


### Core Mechanics

There are a couple of things that are important to know about how barely works. If you've used similar frameworks before, you'll probably already be familiar with most of these things. barely doesn't try to reinvent the wheel.

- the structure of your site is defined in jinja2 templates. By default, these are stored in the `templates/` folder
- you write the contents of your pages with [Markdown](https://guides.github.com/features/mastering-markdown/)
- each page can individually be configured using [YAML notation](https://github.com/charludo/barely/blob/main/docs/detailed-overview.md)
- global level configuration of barely happpens in the `config.yaml` file, global variables to be used in your templates are stored in `metadata.yaml`

This just scratches the surface; please, do yourself a favor and read the [Detailed Overview](https://github.com/charludo/barely/blob/main/docs/detailed-overview.md) in the docs.

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

To see how, when, and why to use them, see here: [Modular Pages](https://github.com/charludo/barely/blob/main/docs/modular-pages.md)

### Plugins

barely offers rather limited functionality on its own: "use some templates to render some contents into static HTML files". That's it.

But most of the time, you will want at least a little more functionality. That's where plugins come in!

barely comes with 10 plugins by default:

- [AutoSEO](https://github.com/charludo/barely/blob/main/docs/plugins/autoseo.md)
- [AutoSummary](https://github.com/charludo/barely/blob/main/docs/plugins/autosummary.md)
- [Collections](https://github.com/charludo/barely/blob/main/docs/plugins/collections.md)
- [Forms](https://github.com/charludo/barely/blob/main/docs/plugins/forms.md)
- [Gallery](https://github.com/charludo/barely/blob/main/docs/plugins/gallery.md)
- [Highlight](https://github.com/charludo/barely/blob/main/docs/plugins/highlight.md)
- [Minify](https://github.com/charludo/barely/blob/main/docs/plugins/minify.md)
- [Pixelizer](https://github.com/charludo/barely/blob/main/docs/plugins/pixelizer.md)
- [Reading Time](https://github.com/charludo/barely/blob/main/docs/plugins/readingtime.md)
- [Timestamps](https://github.com/charludo/barely/blob/main/docs/plugins/timestamps.md)
- [Table of Contents](https://github.com/charludo/barely/blob/main/docs/plugins/toc.md)
- [git](https://github.com/charludo/barely/blob/main/docs/plugins/git.md)
- [Local Backup](https://github.com/charludo/barely/blob/main/docs/plugins/localbackup.md)
- [SFTP](https://github.com/charludo/barely/blob/main/docs/plugins/sftp.md)

For more information on how to enable and configure a plugin, click on its respective name.

To learn how to install new plugins or write your own, see [the Plugins page](https://github.com/charludo/barely/blob/main/docs/plugins.md) in the docs.

### Blueprints

Back in the [Basics](#basics), we have already briefly covered blueprints. They are pretty much exactly what you would expect: re-usable project templates that you can instantiate into new projects. Other frameworks might call them themes.

You can list all available blueprints with:
```console
$ barely blueprints
[barely][  core][ INFO] :: found 2 blueprints:
                        -> default
                        -> blank
```

To learn how to create and use your own blueprints, see [Blueprints](https://github.com/charludo/barely/blob/main/docs/blueprints.md) in the docs.

<!-- ROADMAP -->
## Roadmap

barely is currently released as version `1.0.0`. That means that while everything works and the project is feature complete (in regards to its initial vision), there are still a lot of improvements to be made. The current wishlist is:

- **performance improvements**. barely is fast enough for every-day use, but not exactly optimized. The biggest performance win could probably be made by letting barely interact with a model of the current project, instead of constantly opening / closing the same files. That's a major rework though, and maybe something for version 2.0.0...

- a good demo blueprint, showcasing all of barelys features and plugins

- **the docs** could use some love :)

<!-- CONTRIBUTING -->
## Contributing

Contributors are highly appreciated! Check out [CONTRIBUTING.md](https://github.com/charludo/barely/blob/main/CONTRIBUTING.md) for more info!

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

Distributed under the GNU General Public License. See [LICENSE](https://github.com/charludo/barely/blob/main/LICENSE) for more information.


<!-- CONTACT -->
## Contact

Telegram: [@smiletolerantly](https://t.me/smiletolerantly) - barely@buildwithbarely.org

Official Website Link: [https://buildwithbarely.org](https://buildwithbarely.org)
Github Project Link: [https://github.com/charludo/barely](https://github.com/charludo/barely)

## Changelog
Most recent entry:

## [1.0.5] - 2022-02-23
### Fixed
- autoSEO: fixed double "/" issue in image URLs

### Changed
- silently ignores FileNotFound errors instead of throwing an exception, since usually, a temp file is at fault

See the full changelog [here](https://github.com/charludo/barely/blob/main/CHANGELOG.md)

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/charludo/barely
[contributors-url]: https://github.com/charludo/barely/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/charludo/barely
[forks-url]: https://github.com/charludo/barely/network/members
[stars-shield]: https://img.shields.io/github/stars/charludo/barely
[stars-url]: https://github.com/charludo/barely/stargazers
[issues-shield]: https://img.shields.io/github/issues/charludo/barely
[issues-url]: https://github.com/charludo/barely/issues
[license-shield]: https://img.shields.io/github/license/charludo/barely
[license-url]: https://github.com/charludo/barely/blob/master/LICENSE.txt
[pypi-shield]: https://img.shields.io/pypi/dm/barely
[pypi-url]: https://pypi.org/project/barely/
