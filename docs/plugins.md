# Plugins

barely offers rather limited functionality on its own: "use some templates to render some contents into static HTML files". That's it.

But most of the time, you will want at least a little more functionality. That's where plugins come in!

barely knows three kinds of plugins:

### 1. Content Plugins

These look out for certain file extensions, which they will further process than barely normally would. Some also perform some additional tasks right after you've finished editing the project.

barely ships with:
- [AutoSeo](plugins/autoseo.md): generate SEO-, OpenGraph- and Twitter-relevant tags from a very minimal required information set. Can also generate `robots.txt` and `sitemap.txt` files. Works great with AutoSummary!

- [AutoSummary](plugins/autosummary.md): make use of the NLTK to generate a short summary of a page. Can also extract a list of most relevant keywords

- [Collections](plugins/collections.md): add a page to Collections or request the contents of one (or multiple). Can also generate Collection overview pages. These are barelys version of categories.

- [Forms](plugins/forms.md): specify forms in pure YAML, let the plugin generate their HTML representation!

- [Gallery](plugins/gallery.md): specify a gallery name, sorting, and an image folder in markdown; let the plugin generate a gallery! Works great with Pixelizer!

- [Highlight](plugins/highlight.md): lex & highlight code blocks using pygments! Lets you specify the language and theme on a global, page or code block level.

- [Minify](plugins/minify.md): minify JS files; **compile SASS/SCSS into regular old css!**

- [Pixelizer](plugins/pixelizer.md): turn img-tags in picture-tags, with multiple srcsets for the original image format and webp, all at different target resolutions. Google loves this

- [ReadingTime](plugins/readingtime.md): estimate the reading time for a page or a blog post - a common feature on many blogs.

- [Timestamps](plugins/timestamps.md): lets you automatically display the created or last edited times of pages and posts in a custom time format. Also a common feature on many blogs.

- [Table of Contents](plugins/toc.md): Generate a table of contents and automatically link them to your headings, just like the one at the top of [the README](/README.md)!

### 2. Backup Plugins

After you are done editing your project in live mode or after running `barely rebuild`, back up your changes.

barely ships with:
- [git](plugins/git.md): commit & push all the changes to a remote repository

- [LocalBackup](plugins/localbackup.md): keep a limited number of backups on your local machine. Better than nothing, but git is much preferred.

### 3. Publication Plugins

Publish your changes! Currently only one of these comes bundled with barely:
- [sftp](plugins/sftp.md): copy your webroot to an sftp-server. Handy for making quick changes or quickly publishing a blog post!

---

You might ask yourself, "how do these categories differ from one another?"
- content plugins help process your files
- backup plugins work on your `devroot` after you've finished editing
- publication plugins work on your `webroot` after you've finished editing

*Check the individual plugin documentations for how to configure them, and if they're enabled by default or not.*

## Installing new Plugins

If you wrote your own plugin or got one from somewhere else, installation is straight forward. You will either have a `plugin.py` file, or a `Plugin` directory containing the actual plugin, as well as miscellaneous other ressources and (hopefully) a testsuite for the plugin.

Depending on what kind of plugin it is (Content, Backup or Publication), you simply place the file or folder into the corresponding directory:
```console
~/user/.barely/plugins/content/
~/user/.barely/plugins/backup/
~/user/.barely/plugins/publication/
```

If you are on Windows, that is:
```console
C:\Users\user\AppData\barely\plugins\content\
C:\Users\user\AppData\barely\plugins\backup\
C:\Users\user\AppData\barely\plugins\publication\
```

Depending on the plugin, you might have to enable or configure it in your projects `config.yaml`.

## Writing your own Plugins

Writing a plugin is just as easy and straightforward as its installtion. As an example, let's write a plugin that appends a copyright notice to every page of our website.

Create a new directory and plugin file:
```console
$ mkdir Copyright
$ cd Copyright/
$ touch copyright.py
```

Open `copyright.py` in your favorite editor and fill it with a bit of boilerplate:
```python
from barely.plugins import PluginBase


class Copyright(PluginBase):

  def __init__(self):
    super().__init__()
    pass

  def register(self):
    pass

  def action(self, item):
    pass

  def finalize(self):
    pass
```

What do these functions do? Well, `__init__` currently only makes a call to the `__init__` function of our plugins parent, `PluginBase`. All Plugins **have** to inherit from `PluginBase`, and implement the `register` and `action` functions.

Our `register` function will be called once during barelys initialization, when barely polls all plugins for information on their name, their priority, and what types of files they want to register for.

`action`, finally, will contain our actual plugin logic.

Let's start by fleshing out `__init__`:
```python
def __init__(self):
  super().__init__()
  standard_config = {
    "copyright_notice": "Hey! This website is copyrighted!",
    "priority": 10
  }

  try:
    self.plugin_config = standard_config | self.config["copyright"]
  except KeyError:
    self.plugin_config = standard_config
```
We have created a standard configuration for our plugin: it contains the copyright notice, as well as our plugins priority. The priority can be any positive integer value, and barely sorts plugins in ascending order of their priority.

Next we try to union our `standard_config` with `self.config["copyright"]`. `self.config` actually already exists: it got handed to our plugin when we called `super().__init__()`. This dict contains all the configurations from our `config.yaml`. So if we wanted to show a different notice or change the order in which plugins are called, we could put this into our `config.yaml`:
```yaml
copyright:
  copyright_notice: My very Custom Copyright
  priority: 1
```

**Note:** any plugin with a negative priority will be ignored. That's the preferred method of disabling a plugin: just set its priority to `-1`. Many plugins also have a priority of `-1` by default, so they won't get called unless you manually enable them.

Now let's move on to registration:
```python
def register(self):
  return "Copyright", self.plugin_config["priority"], [self.config["PAGE_EXT"]]
```

- "Copyright" is just the name of our plugin
- `self.plugin_config["PRIORITY"]` will be `10` by default - see our `__init__` method!
- `[self.config["PAGE_EXT"]]` is the list of file extensions that our plugin wants to register for. `PAGE_EXT` is set to `md` by default. You can return an arbitrarily long list of extensions (**without the dot!**). As you can see though, for just one extenion that extension **must** be wrapped in a list.

**Note**: only Content plugins return extensions. Backup and Publication plugins only return a 2-tuple of name and priority.

And with that, we are finally ready to actually *do* something with this plugin!
```python
def action(self, item):
	item["content"] += self.plugin_config["copyright_notice"]
	yield item
```

Wait... that's it?!  
Yep! Our plugin will get handed every single Markdown page in form of an [item](#item)-dict. We simply append our copyright notice to the end of the content of each page.

Note that we don't return the item - we yield it. barely expects a generator object back, so return won't work.

Maybe already you noticed the implications of this: We could actually yield an arbitrary amount of items! If you wanted to, you could (for example) write a plugin that takes a pages content, then Google-translates it into a dozen languages and yields a separate page for each one of them!

---

Here's our finished plugin:
```python
from barely.plugins import PluginBase


class Copyright(PluginBase):

    def __init__(self):
        super().__init__()
        standard_config = {
            "copyright_notice": "Hey! This website is copyrighted!",
            "priority": 10
        }

        try:
            self.plugin_config = standard_config | self.config["copyright"]
        except KeyError:
            self.plugin_config = standard_config

    def register(self):
        return "Copyright", self.plugin_config["priority"], [self.config["PAGE_EXT"]]

    def action(self, *args, **kwargs):
        item["content"] += self.plugin_config["copyright_notice"]
    	yield item

    def finalize(self):
        pass

```

Simply place your Copyright folder into the content plugins directory (see above!) and watch your plugin work when you start and use barely!

You probably noticed that `finalize` is still empty. In fact, feel free to delete it. This function gets called right before barely exits (or has finished re-building) your project, and enables you to run some cleanup tasks should they be necessary.

As an example, the [Collections](plugins/collections.md) plugin utilizes this method to generate category overview pages once you are done editing the project and it can be sure that there are no further changes coming.

## Item

Above, we already mentioned that a plugins `action` function gets passed a page `item` as (the only) argument. This `item` is simply a dict, so you can manipulate any existing entries and create new ones freely. By default, an `item` will look like this:
```yaml
item:
  origin: devroot/path/to/original/file.ext
  destination: webroot/path/to/where/it/goes.ext

  type: PAGE (or IMAGE, TEXT, or GENERIC)
  extension: ext

  content_raw: the raw contents of the origin file
  content: your markdown, converted to HTML
  output: what barely currently plans on writing into the rendered file

  image: if your file is an image, you will find a PIL Image object here
  template: the template used to render this page

  meta:
    modular: a list of subpages, if your page is modular
    no_render: set to true if the page should not be rendered
    ...: all page specific yaml configuration
    ...: global variables from metadata.yaml
    ...: these get **unpacked, so you can use them directly in a template!
```

[< back](README.md)
