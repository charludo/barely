# Timestamps

Type: `content`  
Enabled by default: `false`

Timestamp your pages and posts. Generates stamps for the creation and last modified times. Displays them in a custom time format.

**Note**: On Unix systems, there is no "creation" timestamp. It always gets reset to the last modified time.

---

Display the timestamps like this in your template:
```html
{{ created }}
{{ edited }}
```

---

|argument				|default value		|explanation									|
|-----------------------|-------------------|-----------------------------------------------|
|PRIORITY				|3					|												|
|FORMAT					|%d.%m.%Y			|												|
