# Detailed Overview

There are a couple of things that are important to know about how barely works. If you've used similar frameworks before, you'll probably already be familiar with most of these things. barely doesn't try to reinvent the wheel.

1. Templates:

	- all your templates live in the `templates/` folder inside your devroot. If, for whatever reason, you want to place them somewhere else, set the `TEMPLATES_DIR` variable in your `config.yaml`.

	- you can organize your templates freely inside that folder, including the use of subfolders.

	- you set a template for a page by naming the pages markdown file according to this scheme:

		- you have the following template: `templates/something.html`. To use it, name any markdown file `something.md`.

		- if your template lives in a subfolder, you specify it with a `.`: to use `templates/subdir/other.html`, name your markdown file `subdir.other.md`.

	- templates can include or extend other templates:

		- `{% include "subdir/other.html" %}`

		- `{% extends "something.html" %}`

	- for any additional information regarding templates, please refer to the [official jinja2 documentation](https://jinja.palletsprojects.com/en/3.0.x/).

2. YAML & Markdown

	If you are not familiar with Markdown yet, GitHub has an [excellent guide](https://guides.github.com/features/mastering-markdown/) on it. You will create a Markdown file corresponding to every page of your website.

	Inside of every markdown file, you can specify variables to be used either in some plugin, or in your templates. To do so, the first line of the file has to be `---`, and the same delimiter has to be used before any markdown contents.

	Inbetween the delimiters, you can use normal YAML syntax:
	```yaml
	---
	title: "Page title for use in a template!"
	description: "..."
	nested:
	  - value
	  - something else
	---
	```
	These variables can be used like any others in your templates: `{{ title }}`.

	Here you can also specify if you want your rendered file to have a different extension, for example: `extension: php`.

	Both the initial YAML section and any Markdown are optional. If you want to, your file can be completely empty. In that case, the template specified by the filename will still get rendered as usual.

3. Configuration Files

	You can utilize two configuration files:
	- `config.yaml`: configure barelys behaviour. You have to at least specify the paths to your webroot and devroot, like this:
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

		**Note:** `config.yaml` is also the place for [plugin configurations](plugins.md)

	- `metadata.yaml`: set global variables. You can leave this file empty or completely remove it.

4. Other Files

	Any other files will get copied over into your webroot (possibly after being processed by your enabled plugins), as long as they aren't set to be ignored in your `config.yaml`.

## Modular Pages

See the [Modular Pages](modular-pages.md) page.

## Plugins

See the [Plugins](plugins.md) page.

## Blueprints

See the [Blueprints](blueprints.md) page.

[< back](README.md)
