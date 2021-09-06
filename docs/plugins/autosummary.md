# AutoSummary

Type: `content`  
Enabled by default: `false`

Relies on NLTK, numpy, scipy, networkx, and rake-nltk. Since these are quite heavy dependencies, and NLTK has to download additional corpus data, the plugin is disabled by default and will install and download all dependencies the first time you use it.

You can let the plugin generate a summary and/or a list of keywords for every page.

---

|argument				|default value		|explanation									|
|-----------------------|-------------------|-----------------------------------------------|
|PRIORITY				|20					|												|
|SENTENCES				|3					|length of the summary in sentences				|
|LANGUAGE				|english			|configurable globally and per page				|
|MIN_SENT_LENGTH		|6					|minimum sentence length in words				|
|MAX_KEYWORDS			|10					|maximum number of extracted keyword phrases	|
|KEYWORDS				|false				|enable/disbale keyword extracion				|
|SUMMARY				|true				|enable/disbale summary generation				|
