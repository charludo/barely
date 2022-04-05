# Reading Time

Type: `content`  
Enabled by default: `true`

Estimates the reading time in minutes for a page or post. Common feature for blogs.

If WPM_FAST does not equal WPM_SLOW, displays an estimate of `x - y` minutes. Otherwise, only a single number is displayed.

---

Display the reading time like this in your template:
```html
{{ reading_time }}
```

---
**config.yaml key:** READING_TIME
|argument				|default value		|explanation									|
|-----------------------|-------------------|-----------------------------------------------|
|PRIORITY				|850				|												|
|WPM_FAST				|265				|for fast readers								|
|WPM_SLOW				|90 				|for slow readers								|
|SEPARATOR				| - 				|separator between the fast and slow values		|
