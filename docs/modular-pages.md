# Modular Pages

Sometimes, a page can contain many different sections, all with their own content, structure and design. An example of this are websites in the OnePage style, or with a long landing page. You might have distinct sections, like "About", "Services", and "Contact" on one page. Since there isn't really a way to split the contents of one pages markdown (it will all get rendered into a single `<div></div>`), barely features modular pages.

These differ from normal pages in that they won't get rendered on their own, and thus are not linkable in a menu. Instead, they get "absorbed" into the parent page.

## Defining a modular page

To define a modular page, simply put the "modular" argument into that pages configuration:
```yaml
---
title: My Parent Page
modular:
  - about
  - services
  - contact
---
```

Here, we told barely that our parent page has three children: about, services, and contact. For each of those, barely expects a folder with that exact name, lead by an `underscore`.
Inside those folders, you can define pages and their templates, as well as any additional ressources, just like you would with any normal page.

Notably, the names in our `modular` variable only reflect what the child pages are called, **not** what template they use. So our directory could (for example) look like this,
```console
$ tree .
.
├── _about
│   └── child.md
├── _contact
│   └── contactform.md
├── parent.md
└── _services
    └── child.md
```
where _about and _services share the same template, but _contact does not.

Also note that subpages get handed to plugins just like any other pages! They can not, however, have subpages of their own.

To display the subpages, the template for your parent.md has to look somewhat like this:
```html
{% for sp in sub_pages %}
  {{ sp }}
{% endfor %}
```

You can not access subpages by their name, `sub_pages` is a list containing the rendered subpages, ordered the same way that you specified them in back in the parents YAML.

## Organization

It's good style to keep your modular templates somewhat separate from your normal ones. This is as easy as creating a `modular/` folder inside your `templates/` directory, then naming the subpages like `modular.child.md`.

[< back](README.md)
