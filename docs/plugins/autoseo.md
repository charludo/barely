# AutoSEO

Type: `content`  
Enabled by default: `true`

Generate all the pesky meta-tags from a very limited configuration. This plugin can save you a lot of time, and make your pages much more appealing to Google & Co.

AutoSEO is quite smart about figuring out good values for tags, and has multiple fallback sources for every one of them. Most of the time you will get away with a very basic config (see below).

Set up your `metadata.yaml` like this:

```yaml
site_url: the URL at which you plan on publishing your website
site_name: name of your website
site_description: optional (fallback) if no page-specific description is found
site_keywords: keywords befitting to all pages
favicon: favicon
twitter_site: your twitter profile
twitter_creator: what twitter user to attribute content to. better specified on a per-page-basis.
```

**ALL** of these are optional.

Then make sure you have a `title` specified in the meta of your pages (`site_name` will be used as fallback). Either provide a summary, a description, or let the AutoSummary generate it, as well as extract relevant keywords.

You can specify a title_image, if none is found, the plugin will extract one from your markdown; if none is found again, it will look for one in the page's directory in the devroot.

You can also override these values specifically for social media (OpenGraph/Facebook and Twitter).

All in all, in addition to the above global values, these attributes are respected:

- title
- title_image
- description
- summary
- keywords
- robots
- SEO:
	- title
	- title_image
	- title_image_alt
	- description
	- site_name
	- twitter_card
	- twitter_site
	- twitter_creator
---

Use the generated tags in the `<head>` of your base template:

```HTML
<html>
	<head>
		{{ seo_tags }}
		...
	</head>
	...
</html>
```

If you have not manually created a `robots.txt` and/or `sitemap.txt` already, the plugin will do it for you.

---

|argument				|default value		|explanation									|
|-----------------------|-------------------|-----------------------------------------------|
|PRIORITY				|30					|												|
|MISC_TAGS				|true				|auto-generate charset & viewport tags			|
