# About barely

barely was built out of frustration with the readily available site generators, frameworks and CMS, which mostly fall into two categories: not providing crucial features; or providing such an overload of them that gettig started with the system takes longer than just building the site by hand.

barely won't be the right tool for everyone and every project, and neither does it try to be. But it might be the right tool for your project, if:

* you want to build a static webpage
* you want to do so rapidly, with the barest minimum of setup and configuration
* you value live reloading of every one of your changes, including SCSS/SASS, images and templates
* you are satisfied with the featureset expected of a typical website or blog

In those circumstances, barely aims to give you as smooth an experience as possible, by following these design principles:

## Simplicity

All your files live in one directory (your devroot). You have - at most - two config files, one for configuring barelys behaviour, one for global metadata. You don't have to touch either one if you don't want to.

barely renders markdown content and jinja2 templates into HTML pages. That's it. (OK, that's only it if you deactivate all the awesome [plugins](plugins.md) barely ships with.)

## Workflow

If you start barely by typing `barely live` (or just `barely`), a live server starts and opens your project in your preferred browser. Any changes you save - be it in a page file, its yaml configuration, a template or even CSS/JS/SASS/... get reflected immediately. This makes working a breeze.

When you've finished, simply hit `Ctrl+C`, and press enter on barelys prompt to push your changes to git, publish the site to your sftp server, or any other action you've specified.

Since building performant and SEO-friendly websites is always important, barely comes bundled with a Google **Lighthouse** CLI option, letting you quickly generate reports about your sites health.

## Extensibility

barely comes with 10 [plugins](plugins.md) that make working even easier, like automatically compressing images, compiling SASS, generating complete HTML forms out of yaml, and managing Collections (barelys catch-all term for things like tags or categories of posts and pages).

Should you still miss some functionality, chances are you can implement it in minutes, thanks to barelys super simple [plugins API](plugins.md#writing-your-own-plugins).

[< back](README.md)
