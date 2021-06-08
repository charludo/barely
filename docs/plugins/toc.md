# Table of Contents

Type: `content`  
Enabled by default: `true`

Creates a nicely structured table of contents by assigning IDs to your headings and linking to them. You can specify the min and max levels of headings, and whether it should be an unordered list, an ordered list, or some other wrapper tag should be used.

---

Display the table of contents like this in your template:
```html
{{ toc }}
```

---

|argument				|default value		|explanation									|
|-----------------------|-------------------|-----------------------------------------------|
|PRIORITY				|2					|												|
|MIN_DEPTH				|1					|												|
|MAX_DEPTH				|4					|												|
|LIST_ELEMENT			|ul					|ol for ordered list							|
