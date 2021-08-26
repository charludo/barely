"""
auto-generate a summary of the contents
of a pge, e.g. to use for a meta description

disabled by default due to massive deps
installs deps on first use
"""
import re
import os
import sys
import subprocess
import pkg_resources
from barely.plugins import PluginBase

required = {"nltk", "numpy", "networkx", "scipy", "rake-nltk"}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

if missing:
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)

import nltk
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx
from rake_nltk import Rake


class AutoSummary(PluginBase):

    def __init__(self):
        super().__init__()
        try:
            standard_config = {
                "PRIORITY": 20,
                "SENTENCES": 3,
                "LANGUAGE": "english",
                "MIN_SENT_LENGTH": 6,
                "MAX_KEYWORDS": 10,
                "KEYWORDS": False,
                "SUMMARY": True
            }
            self.plugin_config = standard_config | self.config["AUTO_SUMMARY"]

            data_dir = os.path.join(os.environ["barely_appdir"], ".nltk_data")

            nltk.data.path.append(data_dir)
            nltk.download("stopwords", quiet=True, download_dir=data_dir)
            nltk.download("punkt", quiet=True, download_dir=data_dir)
        except KeyError:
            self.plugin_config = {"PRIORITY": -1}

    def register(self):
        return "AutoSummary", self.plugin_config["PRIORITY"], [self.config["PAGE_EXT"]]

    def action(self, *args, **kwargs):
        if "item" in kwargs:
            item = kwargs["item"]

            # Get the appropriate Stopwords
            try:
                language = item["meta"]["language"]
            except KeyError:
                language = self.plugin_config["LANGUAGE"]

            if "summary" not in item["meta"] and self.plugin_config["SUMMARY"]:
                # Split the content into a list of sentences, each again a list of words
                sentences = nltk.sent_tokenize(item["content_raw"])
                sentences = [nltk.word_tokenize(sentence)[:-1] for sentence in sentences]
                sentences = [s for s in sentences if not len(s) < self.plugin_config["MIN_SENT_LENGTH"]]

                if len(sentences) <= self.plugin_config["SENTENCES"]:
                    item["meta"]["summary"] = item["content_raw"]
                else:
                    sw = stopwords.words(language)

                    # Build a similarity matrix
                    similarity_matrix = np.zeros((len(sentences), len(sentences)))

                    for i in range(len(sentences)):
                        for j in range(len(sentences)):
                            if i == j:
                                continue
                        similarity_matrix[i][j] = self._sentence_similarity(sentences[i], sentences[j], sw)

                    sim_scores = nx.pagerank(nx.from_numpy_array(similarity_matrix))
                    sim_ranking = sorted(((sim_scores[i], s) for i, s in enumerate(sentences)), reverse=True)
                    summary = ". ".join([" ".join(sim_ranking[i][1]) for i in range(self.plugin_config["SENTENCES"])])
                    summary = re.sub(r"\s([\.\!\;\,\?\'\"\:])", lambda match: match.group(1), summary)
                    item["meta"]["summary"] = summary + "."

            if "keywords" not in item["meta"] and self.plugin_config["KEYWORDS"]:
                r = Rake(language=language)
                r.extract_keywords_from_text(item["content_raw"])
                item["meta"]["keywords"] = r.get_ranked_phrases()[:int(self.plugin_config["MAX_KEYWORDS"])]

            yield item

    @staticmethod
    def _sentence_similarity(s1, s2, stopwords):
        s1 = [w.lower() for w in s1]
        s2 = [w.lower() for w in s2]

        dictionary = list(set(s1 + s2))

        def word_frequency(sentence):
            v = [0] * len(dictionary)
            for w in sentence:
                if w in stopwords:
                    continue
                v[dictionary.index(w)] += 1
            return v

        return 1 - cosine_distance(word_frequency(s1), word_frequency(s2))
