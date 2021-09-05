# Highlight

Type: `content`  
Enabled by default: `true`

Lex and highlight `markdown code blocks`. You can configure a global theme and lexer, and then override both in page configs; you can also specify the lexer on a per-code-block-level like this:

	```python

	<your code goes here>
	
	```

---

For a full list of features, check [pygments.org](https://pygments.org/)!

---

|argument			|default value		|explanation									|
|-------------------|-------------------|-----------------------------------------------|
|PRIORITY			|20					|												|
|CLASS_PREFIX		|hl					|in case of conflicting styles					|
|LINE_NOS			|table 				|												|
|TABSIZE			|4					|												|
|ENCODING 			|utf-8				|												|
|THEME				|default			|check pygments.org for a list					|
|LEXER				|					|empty means guessing							|
|ASSETS_DIR			|assets				|where to place theme css files					|
