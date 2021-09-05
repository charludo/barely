"""
auto-generate lots of SEO-relevant tags

...because doing it manually is boring.
"""
import os
import re
import glob
from barely.plugins import PluginBase


class AutoSEO(PluginBase):

    def __init__(self):
        super().__init__()
        standard_config = {
            "PRIORITY": 30,
            "MISC_TAGS": True
        }
        try:
            self.plugin_config = standard_config | self.config["AUTO_SEO"]
        except KeyError:
            self.plugin_config = standard_config
        self.url = ""

    def register(self):
        return "AutoSEO", self.plugin_config["PRIORITY"], [self.config["PAGE_EXT"]]

    def action(self, item):
        if "parent_meta" not in item:
            # 1. extract as much information as possible from the page item
            seo = self._extract_tags(item)

            # 2. do some post-processing & filling in of gaps

            # append the site_title to the title, should they exist;
            # set the site_title as title, should the latter not exist
            if "title" in seo and "site_title" in seo:
                seo["title"] = f"{seo['title']} | {seo['site_title']}"
            if "title" not in seo and "site_title" in seo:
                seo["title"] = seo["site_title"]

            # if no image was specified, find one now
            if "og:image" not in seo:
                try:
                    seo["og:image"] = re.findall(r"<img\b[^>]+?src\s*=\s*['\"]?([^\s'\"?#>]+)", item["content"])[0]
                except IndexError:
                    seo |= self._first_image(os.path.dirname(item["destination"]))

            # find the absolute URL of the image, and
            # compute the og:url from site_url and destination of item
            if "og:url" in seo:
                # keep up to date for finalize
                self.url = seo["og:url"]
                page_path = item["destination"].replace(self.config["ROOT"]["WEB"], "").replace("\\", "/")

                if "og:image" in seo and os.path.isabs(seo["og:image"]):
                    seo["og:image"] = seo["og:url"] + seo["og:image"]
                elif "og:image" in seo and not seo["og:image"].startswith("http"):
                    img_path = os.path.dirname(page_path) + "/" + seo["og:image"]
                    seo["og:image"] = seo["og:url"] + img_path

                seo["og:url"] = seo["og:url"] + page_path

                # 3. generate the meta html tags
                item["meta"]["seo_tags"] = self._generate_tags(seo)

        yield item

    def finalize(self):
        if not self.url:
            # not enough information to continue
            return

        # sitemap.txt
        sitemap_dev = os.path.join(self.config["ROOT"]["DEV"], "sitemap.txt")
        sitemap_web = os.path.join(self.config["ROOT"]["WEB"], "sitemap.txt")
        sitemap_url = self.url + "/" + "sitemap.txt"

        if not os.path.exists(sitemap_dev):
            pages = glob.glob(os.path.join(self.config["ROOT"]["WEB"], "**", "*.html"), recursive=True)
            pages = [f.replace(self.config["ROOT"]["WEB"], self.url).replace("\\", "/") for f in pages]
            pages = "\n".join(pages)

            with open(sitemap_web, "w") as file:
                file.write(pages)

        # robots.txt
        robots_dev = os.path.join(self.config["ROOT"]["DEV"], "robots.txt")
        robots_web = os.path.join(self.config["ROOT"]["WEB"], "robots.txt")

        if not os.path.exists(robots_dev):
            robots = f"User-agent: *\nAllow: /\n\nSitemap: {sitemap_url}"

            with open(robots_web, "w") as file:
                file.write(robots)

    @staticmethod
    def _extract_tags(item):
        try:
            page_seo = item["meta"]["SEO"]
        except KeyError:
            page_seo = {}

        # Page-specific metadata; already merged with global metadata in ProcessingPipeline!
        def get_page(tag, rebrand=None):
            rebrand = rebrand if rebrand else tag
            if tag in item["meta"]:
                return {rebrand: item["meta"][tag]}
            return {}

        # Page & SEO specific metadata, can differ from page-specific one
        def get_seo(tag, rebrand=None):
            rebrand = rebrand if rebrand else tag
            if tag in page_seo:
                return {rebrand: page_seo[tag]}
            return {}

        seo = {}

        # extract all the necessary info, from wherever we can get it
        # rightmost is preferred

        # title
        seo |= get_page("title")
        # description
        seo |= get_page("site_description", "description") | get_page("summary", "description") | get_page("description")
        # robots
        seo |= {"robots": "all"} | get_page("robots")
        # keywords
        keywords = item["meta"]["keywords"] if "keywords" in item["meta"] else []
        site_keywords = item["meta"]["site_keywords"] if "site_keywords" in item["meta"] else []
        seo |= {"keywords": ", ".join(list(set(site_keywords) | set(keywords)))}
        # favicon
        seo |= get_page("favicon")

        # og:title
        seo |= get_page("title", "og:title") | get_seo("title", "og:title")
        # og:description
        seo |= get_page("site_description", "og:description") | get_page("summary", "og:description") | get_page("description", "og:description") | get_seo("description", "og:description")
        # og:image
        seo |= get_page("title_image", "og:image") | get_seo("title_image", "og:image")
        # og:url
        seo |= get_page("site_url", "og:url")
        # og:site_name
        seo |= get_page("title", "og:site_name") | get_page("site_name", "og:site_name") | get_seo("site_name", "og:site_name")

        # twitter:image:alt
        seo |= get_page("site_description", "twitter:image:alt") | get_page("summary", "twitter:image:alt") | get_page("description", "twitter:image:alt") | get_seo("description", "twitter:image:alt") | get_page("title_image_alt", "twitter:image:alt") | get_seo("title_image_alt", "twitter:image:alt")
        # twitter:card
        seo |= {"twitter:card": "summary_card_large"} | get_seo("twitter_card", "twitter:card")
        # twitter:site
        seo |= get_page("twitter_site", "twitter:site") | get_seo("twitter_site", "twitter:site")
        # twitter:creator
        seo |= get_page("twitter_creator", "twitter:creator") | get_seo("twitter_creator", "twitter:creator")

        return seo

    def _generate_tags(self, seo):
        tags = []

        if self.plugin_config["MISC_TAGS"]:
            tags.append('<meta charset="utf-8" />')
            tags.append('<meta name="viewport" content="width=device-width, initial-scale=1" />')

        if "title" in seo and "og:site_name" in seo:
            tags.append(f'<title>{seo["title"]} | {seo["og:site_name"]}</title>')
        elif "title" in seo:
            tags.append(f'<title>{seo["title"]}</title>')
        elif "og:site_name" in seo:
            tags.append(f'<title>{seo["og:site_name"]}</title>')
        if "description" in seo:
            tags.append(f'<meta name="description" content="{seo["description"][:159]}" />')
        if "keywords" in seo:
            tags.append(f'<meta name="keywords" content="{seo["keywords"]}" />')
        if "robots" in seo:
            tags.append(f'<meta name="robots" content="{seo["robots"]}" />')
        if "favicon" in seo:
            tags.append(f'<link rel="shortcut icon" type="image/x-icon" href="{seo["favicon"]}">')

        if "og:title" in seo:
            tags.append(f'<meta property="og:title" content="{seo["og:title"]}">')
        if "og:description" in seo:
            tags.append(f'<meta property="og:description" content="{seo["og:description"][:159]}">')
        if "og:image" in seo:
            tags.append(f'<meta property="og:image" content="{seo["og:image"]}">')
        if "og:url" in seo:
            tags.append(f'<meta property="og:url" content="{seo["og:url"]}">')
        if "og:site_name" in seo:
            tags.append(f'<meta property="og:site_name" content="{seo["og:site_name"]}">')

        if "twitter:image:alt" in seo:
            tags.append(f'<meta name="twitter:image:alt" content="{seo["twitter:image:alt"][:159]}">')
        if "twitter:site" in seo:
            tags.append(f'<meta name="twitter:site" content="{seo["twitter:site"]}">')
        if "twitter:creator" in seo:
            tags.append(f'<meta name="twitter:creator" content="{seo["twitter:creator"]}">')
        if "twitter:card" in seo:
            tags.append(f'<meta name="twitter:card" content="{seo["twitter:card"]}">')

        return "\n".join(tags)

    def _first_image(self, path):
        images = []
        types = [os.path.join(path, f"*.{t}") for t in self.config["IMAGE_EXT"]]
        for files in types:
            images.extend(glob.glob(files))

        if len(images):
            return {"og:image": images[0].replace(self.config["ROOT"]["WEB"], "").replace("\\", "/")}
        return {}
