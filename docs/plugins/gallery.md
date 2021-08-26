# Gallery

Type: `content`  
Enabled by default: `true`

Turn simple markdown into a list of images (aka, a gallery).

Default priority is lower than that of Pixelizer, meaning the Gallery will receive the full optimization benefits of Pixelizer.

---

Markdown-Syntax:

```md
[name <sort> <direction>]!!(image-folder)
```

The name of the gallery and the image folder are required. Sorting key and direction are optional; however, it is not possible to specify `direction` without `sort`, since these are positional arguments.

---

|argument			|default value		|explanation									|
|-------------------|-------------------|-----------------------------------------------|
|PRIORITY			|2					|												|
|DEFAULT_SORT       |name               |name or time                                   |       
|DEFAULT_DIRECTION  |asc                |asc or desc                                    |
|GALLERY_CLASS      |gallery            |class for the wrapping `div`                   |

The wrapping `<div>` also gets an ID of `gallery-{name}`.
