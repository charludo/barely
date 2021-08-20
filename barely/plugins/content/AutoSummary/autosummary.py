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

required = {"nltk", "numpy", "networkx", "scipy"}
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


class AutoSummary(PluginBase):
    # very rough estimate of the reading time in minutes

    def __init__(self):
        super().__init__()
        try:
            standard_config = {
                "PRIORITY": 20,
                "SENTENCES": 3,
                "LANGUAGE": "english"
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

            if "summary" in item["meta"]:
                yield item
                return

            # Split the content into a list of sentences, each again a list of words
            sentences = nltk.sent_tokenize(item["content_raw"])
            sentences = [nltk.word_tokenize(sentence)[:-1] for sentence in sentences]

            if len(sentences) <= self.plugin_config["SENTENCES"]:
                item["meta"]["summary"] = item["content_raw"]
                yield item
                return

            # Get the appropriate Stopwords
            try:
                language = item["meta"]["language"]
            except KeyError:
                language = self.plugin_config["LANGUAGE"]

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
            summary = re.sub(r"\s([\.!;,\?\'\"\[\]\{\}\(\)])", lambda match: match.group(1), summary)
            item["meta"]["summary"] = summary + "."
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
