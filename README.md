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
    <a href="https://github.com/charludo/barely"><strong>Explore the docs »</strong></a>
    <br />
    <br />
	<a href="#plugins">See available Plugins »</a>
	.
    <a href="https://github.com/charludo/barely">Get started »</a>
    ·
    <a href="https://github.com/charludo/barely/issues">Report Bug »</a>
    ·
    <a href="https://github.com/charludo/barely/issues">Request Feature »</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a>
		<ul>
			<li><a href="#basics">Basics</a></li>
			<li><a href="#detailed-overview">Detailed Overview</a></li>
			<li><a href="#plugins">Plugins</a></li>
			<li><a href="#blueprints">Blueprints</a></li>
		</ul>
	</li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

barely was built out of frustration with the readily available site generators, frameworks and CMS, which mostly fall into two categories: not providing crucial features; or providing such an overload of them that gettig started with it takes longer than just building the site by hand.

barely won't be the right tool for everyone and every project, and neither does it try to be. But it might be the right tool for your project, if:

* you want to build a static webpage
* you want to do so rapidly, with the barest minimum of setup and configuration
* you value live reloading of every one of your changes, including SCSS/SASS, images and templates
* you are satisfied with the feature set of a typical website or blog

In those circumstances, barely aims to give you as smooth an experience as possible, by following these design principles:

### Simplicity

All your files live in one directory (your devroot). You have - at most - two config files, one for configuring barely's behaviour, one for global metadata. You don't have to touch either one if you don't want to.

barely renders markdown content and jinja2 templates into HTML pages. That's it. (OK, that's it only if you deactivate all the awesome [plugins](#plugins) barely ships with.)

### Workflow

If you start barely by typing `barely live` (or just `barely`), a live server starts and opens your project i your preferred browser. Any changes you save - be it in a page file, its yaml configuration, a template or even CSS/JS/SASS/... get reflected immediately. This makes working on a project a breeze.

When you've finished, simply hit `Ctrl+C`, and press enter on barely's prompt to push your changes to git, publish the site to your sftp server, or any other action you've specified.

### Extensibility

barely comes with 10 [plugins](#plugins) that make working even easier, like automatically compressing images, compiling SASS, generating complete HTML forms out of yaml, and managing Collections (barely's catch-all term for things like tags or categories on posts and pages).

Should you still miss some functionality, chances are you can implement it in minutes, thanks to barely's super simple [plugin API](#).

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

<!-- GETTING STARTED -->
## Getting Started

Good news: Getting started with barely is easy!

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
	What happened? barely is telling us that we aren't currently in a barely project directory. For a direcctory to count as a project, it has to contain a `config.yaml` file, which in turn has to specify the devroot (where we will work) and the webroot (where barely renders to).

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
	Sweet! barely created two new subdirs, `devroot` and `webroot`. The project was also created with a blueprint, namely `default`, which is why our `devroot` is not empty. We will learn about blueprints in a second.

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
	- `config.yaml` contains all the configuration for barely and its plugins. Right now, it only contains the absolute paths for the devroot and webroot.
	- `metadata.yaml` is a place you can put any values you want to use in multiple places across your project, be it metadata or anythin else
	- `template.md` is the markdown file for the root page of the website. Its content will get rendered into webroot/index.html with the templates/template.md template.
	- `templates/` contains all your templates

6. Let's build the project!
	```console
	$ barely rebuild
	barely :: registering plugins...
	barely :: 8 plugins registered.
	barely :: starting full rebuild...
	       :: deleted [...]/test/webroot
	barely :: event at [...]/test/devroot/template.md
	       :: rendered, highlighted [...]/template.md -> [...]/webroot/index.html
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

When you feel comfortable with the workings of barely, move on to the next section.


### Core Mechanics

There are a couple of things that are important to know. If you've used similar frameworks before, you'll probably already be familiar with most of them. barely doesn't try to reinvent the wheel.

1. Templates:

	- all your templates live in the `templates/` folder inside your devroot. If, for whatever reason, you want to place them somewhere else, set the `TEMPLATES_DIR` variable in your `config.yaml`.

	- you can organize your templates freely inside that folder, including subfolders.

	- you set a template for a page by naming the page's markdown file according to this scheme:

		- you have the following template: `templates/something.html`. To use it, name any markdown file `something.md`.

		- if your template lives in a subfolder, you specify it with a `.`: to use `templates/subdir/other.html`, name your markdown file `subdir.other.md`.

	- templates can include or extend other templates:

		- `{% include "subdir/other.html" %}`

		- `{% extends "something.html" %}`

	- for anything else regarding templates, please refer to the [official jinja2 documentation](https://jinja.palletsprojects.com/en/3.0.x/)

2. YAML & Markdown

	If you're not familiar with Markdown yet, GitHub has an [excellent guide](https://guides.github.com/features/mastering-markdown/) on it.

	Inside of every markdown page, you can specify variables either for use by some plugin, or in your templates. To do so, the first line of the file has to be `---`.
	Afterwards, use normal YAML syntax:
	```yaml
	---
	title: "Page title for use in a template!"
	description: "..."
	nested:
	  - value
	  - something else
	---
	```
	These variables can be used like this in your templates: `{{ title }}`.

	Both the initial YAML section and any Markdown are completely optional. If you want to, your file can be completely empty. In that case, the template specified by the filename will still get rendered as usual.

3. Configuration Files

	You can utilize two configuration files:
	- `config.yaml`: configure barely's behaviour. You have to at least specify the paths to your webroot and devroot, like this:
		```yaml
		ROOT:
			DEV: /[...]/devroot
			WEB: /[...]/webroot
		```

		barely also sets some standard values which you can optionally override:
		```yaml
		TEMPLATES_DIR: templates
		PAGE_EXT: md
		IMAGE_EXT:
		    - jpg
		    - jpeg
		    - png
		IGNORE:
		    - .git
		```

		**Note:** `config.yaml` is also the place for [plugin configurations](3plugins)

	- `metadata.yaml`: set global variables. You can leave this file empty or completely remove it.

4. Other Files

	Any other files will get copied over into your webroot (possibly after being processed by your enabled plugins), as long as they aren't set to be ignored in your `config.yaml`.

### Plugins

barely offers rather limited functionality on its own: use some templates to render some contents into static HTML files.

But most of the time, you will want at least a little more functionality. That's where plugins come in!

barely knows three kinds of plugins:

1. **Content Plugins:** these look out for certain file extensions, which they will further process than barely normally would. Some also perform some additional tasks right after you're finished editing the project.

	barely ships with:
	- [Collections](#): add a page to collections or request the contents of one (or multiple). Can also generate Collection overview pages.
	- [Forms](#): specify forms in pure YAML, let the plugin generate its HTML representation!
	- [Highlight](#): lex & highlight code blocks using pygments! Lets you specify the language and theme on a global, page or code block level.
	- [Minimizer](#):
		- minimize JS files
		- compress & resize images
		- **copile SASS/SCSS int regular old css!**
	- [ReadingTime](#): estimate the reading time for a page or a blog post - a common feature on many blogs.
	- [Timestamps](#): lets you automatically display the created or last edited times of pages and posts in a custom time format. Also a common feature on many blogs.
	- [Table of Contents](#): Generate a table of contents and automatically link them to your headings, just like the one at the top of this page!

2. *##*Backup Plugins:** after you are done editing your project in live mode or after running `barely rebuild`, back up your changes.

	barely ships with:
	- [git](#): commit & push all the changes to a remote repository
	- [LocalBackup](#): keep a limited number of backups on your local machine. Better then nothing, but git is much preferred.

3. **Publication Plugins:** publish your changes! Currently only one of these comes bundled with barely:
	- [sftp](#): copy your webroot to an sftp-server. Handy for making quick changes or quickly publishing a blog post!

You might ask yourself, "how do these categories differ from one another?"
- content plugins help process your files
- backup plugins work on your `devroot` after you're finished editing
- publication plugins work on your `webroot` after you're finished editing

*Check the individual plugin documentations for how to configure them, and if they're enabled by default or not.*

### Writing your own Plugins

A detailed guide would bust the scope of this readme, so [check here for that](#). However, note that it's really quite simple, and after writing it, all you have to do is place it in a special folder in your home directory.

### Blueprints

Back in the [Basics](#basics), we have already briefly covered blueprints. They are pretty much exactly what you would expect: re-usable projects that you can instantiate into new projects.

You can list available blueprint with:
```console
$ barely blueprints
barely :: found 2 blueprints:
	-> default
	-> blank
```

The help menu hints at a way to also create your own blueprints:
```console
$ barely blueprints --help
Usage: barely blueprints [OPTIONS]

  list all available blueprints, or create a new one

Options:
  -n, --new TEXT  create a reusable blueprint from the current project
  --help          Show this message and exit.
```

Executing `barely blueprints --new "name"` will create a new blueprint out of your current project, and you can freely use it from now on:

```console
$ barely blueprints
barely :: found 2 blueprints:
	-> default
	-> blank
	-> name
```

<!-- ROADMAP -->
## Roadmap

barely is currently released as version `1.0.0`. That means that while everything works and the project is feature complete (in regards to its initial vision), there are still a lot of improvements to be made. Some important ones are:

- **better exception handling**. There are numerous ways to get an exception right now (for example: try renaming a page to a non-existant template) that really don't have to cause barely to exit.

- **better logging** - or really, *logging*. Currently, instead of a proper logger, barely just sometimes calls `print()`. Different levels of logging and some color are desperately needed.

- **performance improvements**. barely is fast enough for every-day use, but not exactly optimized. The biggest performance win could probably be made by letting barely interact with a model of the current project, instead of constantly opening / closing the same files. That's a major rework though, and maybe something for version 2.0.0...

- **the docs** could use some love :)

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place. Any contributions you make are **very** much welcome!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/NewFeature`)
3. Commit your Changes (`git commit -m 'Add some NewFeature'`)
4. Push to the Branch (`git push origin feature/NewFeature`)
5. Open a Pull Request

**If you have written a plugin or created a blueprint and think others might benefit, please do share via the same way!!**



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
