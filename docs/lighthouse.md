# Lighthouse

Google Lighthouse is an open-source project that can generate highly insightful metrics about a single page of your website. These metrics contain scores about the SEO-friendliness of your site, its accessibility, and much more.

[Learn more about it here.](https://developers.google.com/web/tools/lighthouse)

There is no native python implementation for Lighthouse, rather, if you want to use it, you will have to have the following installed:

- node
- [lighthouse](https://www.npmjs.com/package/lighthouse) (npm package)
- Chrome or Chromium

These are **not** dependencies of barely. You only have to install these if you want to use Lighthouse.

To generate a report of your root page:
```console
$ barely lighthouse
[barely][  core][ INFO] :: Starting evaluation using lighthouse 8.3.0...
[barely][  core][ INFO] :: Finished the evaluation! Opening the result now.
```

Or specify any other page to be evaluated:
```console
$ barely lighthouse --help
Usage: barely lighthouse [OPTIONS]

  use Google Lighthouse to evaluate a page for SEO- and accessibility scores

Options:
  -p, --page TEXT  specify a page to be evaluated other than the root
  --help           Show this message and exit.
```

[< back](README.md)
