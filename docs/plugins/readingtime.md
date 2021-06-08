# Reading Time

Type: `content`  
Enabled by default: `true`

Estimates the reading time for a page or post. Common feature for blogs

---

Use the reading time like this in your template:
```html
{{ reading_time }}
```

---

|argument				|default value		|explanation									|
|-----------------------|-------------------|-----------------------------------------------|
|PRIORITY				|850				|												|
|WPM_FAST				|265				|for fast readers								|
|WPM_SLOW				|90 				|for slow readers								|
|SEPARATOR				| - 				|separator between the fast and slow values		|
