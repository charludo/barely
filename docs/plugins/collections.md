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
{% for exhibit in exhibits %}
  {% for collectible in exhibit %}
    {{ collectible["title"] }}
    {{ collectible["preview"] }}
    {{ collectible["href"] }}
  {% endfor %}
{% endfor %}
```

Exhibits contain the following tags / information:
```yaml
title: title of the exhibit
preview: the first few words of the page
raw: the entire markdown content of the page
href: link to the page
image: link to image, if title_image was specified on the original page
date: modification or creation time of the page
reading_time: reading time as provided by ReadingTime plugin
```

Inside the OVERVIEW_TEMPLATE, list the available collections like this:
```html
{% for collection in collections_list %}
    {{ collection["name"] }}
    {{ collection["size"] }}
    {{ collection['href'] }}
{% endfor %}
```
where the `size` is the number of collectibles in the collection.

---
**config.yaml key:** COLLECTIONS
|argument			|default value		|explanation									                                          |
|-------------------|-------------------|-----------------------------------------------------------------------------------------|
|PRIORITY			|999				|												                                          |
|PAGE				|categories			|where collection overview pages get rendered to                                          |
|SUMMARY_LENGTH		|100				|cut-off for summaries of pages / posts			                                          |
|OVERVIEW_TITLE		|					|title of the collections overview page  		                                          |
|OVERVIEW_TEMPLATE	|					|template for the collections overview			                                          |
|OVERVIEW_CONTENT	|					|points to markdown file containingcontent of OVERVIEW page                               |
|COLLECTION_TEMPLATE|					|template for the individual collection pages	                                          |
|ORDER_KEY          |timestamp          |specify a key by which	collectibles are sorted on collection pages and within exhibitions|
|ORDER_REVERSE      |true               |reverses the sorting order                                             	              |
