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
    <li><a href="#acknowledgements">Acknowledgements</a></li>
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
> Python 3.9.x
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
	<li><a href="#detailed-overview">Detailed Overview</a></li>
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
> barely :: could not find 'config.yaml'. Exiting
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
barely new --help
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


<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/charludo/barely/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Your Name - [@your_twitter](https://twitter.com/your_username) - email@example.com

Project Link: [https://github.com/your_username/repo_name](https://github.com/your_username/repo_name)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* [GitHub Emoji Cheat Sheet](https://www.webpagefx.com/tools/emoji-cheat-sheet)
* [Img Shields](https://shields.io)
* [Choose an Open Source License](https://choosealicense.com)
* [GitHub Pages](https://pages.github.com)
* [Animate.css](https://daneden.github.io/animate.css)
* [Loaders.css](https://connoratherton.com/loaders)
* [Slick Carousel](https://kenwheeler.github.io/slick)
* [Smooth Scroll](https://github.com/cferdinandi/smooth-scroll)
* [Sticky Kit](http://leafo.net/sticky-kit)
* [JVectorMap](http://jvectormap.com)
* [Font Awesome](https://fontawesome.com)





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
