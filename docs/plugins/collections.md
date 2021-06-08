# Collections

Type: `content`  
Enabled by default: `false`

Collections allow you to include previews of other pages on a page, or to add your page to a collection.  
**Note**: might not update properly during live mode, but will catch up when quitting barely.

---

Add a page to collections like this:
```yaml
collections:
  - col1
  - col2
```

Exhibit pages belonging to collections like this:
```yaml
exhibits:
  - col3
  - col4
```

You can then display exhibits in your templates:
```html
{% for collection in exhibits %}
  {% for exhibit in exhibits %}
    {{ exhibit["title"] }}
    {{ exhibit["preview"] }}
    {{ exhibit["href"] }}
  {% endfor %}
{% endfor %}
```

Exhibits contain the following tags / information:
```yaml
title: title of the exhibit
preview: the first few words of the page
href: link to the page
title_image: link to image, if title_image was specified on the original page
date: modification or creation time of the page
reading_time: reading time as provided by ReadingTime plugin
```

---

|argument			|default value		|explanation									|
|-------------------|-------------------|-----------------------------------------------|
|PRIORITY			|999				|												|
|PAGE				|categories			|where collection overview pages get rendered to|
|OVERVIEW_TITLE		|					|title of the collections overview page  		|
|OVERVIEW_TEMPLATE	|					|template for the collections overview			|
|COLLECTION_TEMPLATE|					|template for the individual collection pages	|
|SUMMARY_LENGTH		|100				|cut-off for summaries of pages / posts			|
