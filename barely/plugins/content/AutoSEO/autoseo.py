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
            "AUTO_KEYWORDS": False
        }
        try:
            self.plugin_config = standard_config | self.config["AUTO_SEO"]
        except KeyError:
            self.plugin_config = standard_config

    def register(self):
        return "AutoSEO", self.plugin_config["PRIORITY"], ["yaml", self.config["PAGE_EXT"]]

    def action(self, *args, **kwargs):
        if "item" in kwargs:
            item = kwargs["item"]

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
            seo |= get_page("site_keywords")
            seo |= get_page("keywords")
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
            seo |= {"twitter:card": "summary_card_large"} | get_page("twitter_card", "twitter:card") | get_seo("twitter_card", "twitter:card")
            # twitter:site
            seo |= get_page("twitter_site", "twitter:site") | get_seo("twitter_site", "twitter:site")
            # twitter:creator
            seo |= get_page("twitter_creator", "twitter:creator") | get_seo("twitter_creator", "twitter:creator")

            # union the keywords and site_keywords, should they exist
            if "keywords" in seo:
                keywords = seo["keywords"]
            elif self.plugin_config["AUTO_KEYWORDS"]:
                keywords = self._extract_keywords(item["content_raw"])
            else:
                keywords = []

            if "site_keywords" in seo:
                keywords = list(set(keywords) | set(seo["site_keywords"]))

            if len(keywords):
                seo["keywords"] = ", ".join(keywords)

            # append the site_title to the title, should they exist;
            # set the site_title as title, should the latter not exist
            if "title" in seo and "site_title" in seo:
                seo["title"] = f"{seo['title']} | {seo['site_title']}"
            if "title" not in seo and "site_title" in seo:
                seo["title"] = seo["site_title"]

            # if no image was specified, find one now
            if "og:image" not in seo:
                try:
                    seo["og:image"] = re.findall(r"<img\b[^>]+?src\s*=\s*['\"]?([^\s'\"?#>]+)", item["content"])[0].group(1)
                except IndexError:
                    image = self._first_image(os.path.dirname(item["destination"]))
                    if image:
                        seo["og:image"] = image.replace(self.config["ROOT"]["WEB"], "").replace("\\", "/")

            # find the absolute URL of the image, and
            # compute the og:url from site_url and destination of item
            if "og:url" in seo:
                page_path = item["destination"].replace(self.config["ROOT"]["WEB"], "").replace("\\", "/")

                if os.path.isabs(seo["og:image"]):
                    seo["og:image"] = seo["og:url"] + seo["og:image"]
                else:
                    img_path = os.path.dirname(page_path) + seo["og:image"]
                    seo["og:image"] = seo["og:url"] + img_path

                seo["og:url"] = seo["og:url"] + page_path

            yield item

    def finalize(self):
        # robots.txt
        # sitemap.txt
        pass

    def _first_image(self, path):
        images = []
        types = [os.path.join(path, f"*.{t}") for t in self.config["IMAGE_EXT"]]
        for files in types:
            images.extend(glob.glob(files))

        if len(images):
            return images[0]
        return None

    @staticmethod
    def _extract_keywords(text):
        return []
