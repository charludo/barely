# Pixelizer

Type: `content`  
Enabled by default: `false`

- compress and resize images (png, jpg, jpeg, tif, tiff, bmp)
- also convert these images to webp
- turn `<img>` tags in markdown files into `<picture>` tags in HTML, offering webp (and the original format as a fallback) to the browser
- targets for resizing/compression, as well as the layouts of the `<picture>` tag, are configurable freely


---

|argument	   |default value	   |explanation									|
|--------------|-------------------|--------------------------------------------|
|PRIORITY	   |3                  |											|
|TARGETS	   |- lg 1000 70<br>- md 650 70<br>- sm 300 70|syntax: \<img-name-suffix\> \<width in px\> \<quality in %\>|
|LAYOUTS	   |- (max-width: 1000px) 100vw<br>- 1000px |these are essentially media queries. Wrap in `"..."` in yaml! |

With the standard config, this:

```md
![Test Image](some/source.jpg)
```

will be turned into this:

```HTML
<picture>
	<source sizes="(max-width: 1000px) 100vw, 1000px" srcset="some/source-lg.webp 1000w, some/source-md.webp 650w, some/source-sm.webp 300w" type="image/webp">
	<source sizes="(max-width: 1000px) 100vw, 1000px" srcset="some/source-lg.jpg 1000w, some/source-md.jpg 650w, some/source-sm.jpg 300w" type="image/jpg">
	<img src="some/source.jpg" alt="Test Image">
</picture>
```

instead of this:

```HTML
<img alt="Test Image" src="some/source.jpg" />
```

Additionally, all 6 variants will be created (resized, quality changed, format changed), and the original will be copied as fallback.
