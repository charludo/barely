# Plugins

barely offers rather limited functionality on its own: use some templates to render some contents into static HTML files.

But most of the time, you will want at least a little more functionality. That's where plugins come in!

barely knows three kinds of plugins:

1. **Content Plugins:** these look out for certain file extensions, which they will further process than barely normally would. Some also perform some additional tasks right after you're finished editing the project.

	barely ships with:
	- [Collections](#): add a page to collections or request the contents of one (or multiple). Can also generate Collection overview pages.
	- [Forms](#): specify forms in pure YAML, let the plugin generate its HTML representation!
	- [Highlight](#): lex & highlight code blocks using pygments! Lets you specify the language and theme on a global, page or code block level.
	- [Minimizer](#):
		- minimize JS files
		- compress & resize images
		- **copile SASS/SCSS int regular old css!**
	- [ReadingTime](#): estimate the reading time for a page or a blog post - a common feature on many blogs.
	- [Timestamps](#): lets you automatically display the created or last edited times of pages and posts in a custom time format. Also a common feature on many blogs.
	- [Table of Contents](#): Generate a table of contents and automatically link them to your headings, just like the one at the top of this page!

2. **Backup Plugins:** after you are done editing your project in live mode or after running `barely rebuild`, back up your changes.

	barely ships with:
	- [git](#): commit & push all the changes to a remote repository
	- [LocalBackup](#): keep a limited number of backups on your local machine. Better then nothing, but git is much preferred.

3. **Publication Plugins:** publish your changes! Currently only one of these comes bundled with barely:
	- [sftp](#): copy your webroot to an sftp-server. Handy for making quick changes or quickly publishing a blog post!

You might ask yourself, "how do these categories differ from one another?"
- content plugins help process your files
- backup plugins work on your `devroot` after you're finished editing
- publication plugins work on your `webroot` after you're finished editing

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

Writing a plugin is just as easy and straightforward as its installtion. For an example, let's write a plugin that appends a copyright notice to every page of your website.

Create a new directory and plugin file:
```console
$ mkdir Copyright
$ cd Copyright/
$ touch copyright.py
```

Open copyright.py in your favorite editor and fill it with a bit of boilerplate:
```python
from barely.plugins import PluginBase


class Copyright(PluginBase):

    def __init__(self):
        super().__init__()
        pass

    def register(self):
        pass

    def action(self, *args, **kwargs):
        pass

	def finalize(self):
		pass
```

What do these functions do? Well, __init__ currently only makes a call to the __init__ function in our plugins parent, `PluginBase`. All Plugins **have** to inherit from `PluginBase`.
Our register function will be called once during barelys initialization, when barely polls all plugins for information on their name, their priority, and what types of files they want to register for.
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

Next we try to override our standard_config with self.config["copyright"]. `self.config` actually already exists: it gets handed to our plugin when we called `super().__init__()`. This dict contains all the configurations from our `config.yaml`! So if we wanted to show a different notice or change the order of plugins around, we could put this into our `config.yaml`:
```yaml
copyright:
	copyright_notice: My very Custom Copyright
	priority: 1
```

**Note:** any plugin with a negative priority will get ignored. That's the referred method of disabling plugins: just set their priority to -1. Many plugins also have a priority of -1 by default, so they won't get executed unless you manually enable them.

Now let's move on to registration:
```python
def register(self):
	return "Copyright", self.plugin_config["PRIORITY"], [self.config["PAGE_EXT"]]
```

- "Copyright" is just the name of our plugin.
- self.plugin_config["PRIORITY"] will return 10 by default - see our `__init__` method!
- [self.config["PAGE_EXT"]] now tells barely that our plugin is only interested in files with a extension of "PAGE_EXT" - by default, this means `.md` files. You can return an arbitrary amount of page extensions (**without the dot!**) as a list. As you can see though, even for just one extenion the type of the returned argument **must** be a list.

And with that, we are ready to actually *do* something with this plugin!
```python
def action(self, *args, **kwargs):
	item["content"] += self.plugin_config["copyright_notice"]
	yield item
```

Wait... that's it?!
Yep! Our plugin will get handed every single Markdown page in form of an [item](#item)-dict. We simply append our copyright notice to the end of the content of each page.

Note that we don't return the item - we yield it. barely expects a generator object back, so return won't work. Maybe you notice the implications of this already: We could actually yield an arbitrary amount of items! If you wanted to, you could (for example) write a plugin that takes a pages content, then Google-translates it into a dozen languages and yields a separate page for each one of them!

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
        return "Copyright", self.plugin_config["PRIORITY"], [self.config["PAGE_EXT"]]

	def action(self, *args, **kwargs):
		item["content"] += self.plugin_config["copyright_notice"]
		yield item

	def finalize(self):
		pass
```

Simply place your Copyright dir into the content plugins folder (see above!) and watch your plugin work when you start and use barely!

You probably noticed that `finalize` is still empty. In fact, feel free to delete it. This function gets called right before barely exists (or has finished re-building) your project, and enables you to run some cleanup tasks should they be necessary. As an example, the [Collections](plugins/collections.md) plugin utilizes this method to generate category overview pages once you are done editing the project and it can be sure that there are no further changes coming.

## Testing your Plugin

It's a good idea to write tests for your plugins. To do so, create a file alongside your plugin file with a leading `test_`, so for example: `test_copyright.py`.

It should look similar to this:
```python
import unittest
from barely.plugins.content.Copyright.copyright import Copyright


class TestCopyright(unittest.TestCase):

    def test_action(self):
		pass	# put your unittests here!
```
The tests will automatically be discovered and run when you `barely test`.

## Item

Above, we already mentioned that a plugins action() function gets passed a page `item`. This is simply a dict, and you can manipulate any existing entries, and create new ones freely. By default, an `item` will look like this:
```yaml
item:
  - origin: devroot/path/to/original/file.ext
  - destination: webroot/path/to/where/it/goes.ext

  - type: PAGE (or IMAGE, TEXT, or GENERIC)
  - extension: ext

  - content_raw: the raw contents of the origin file
  - content: your markdown, converted to HTML
  - output: what barely currently plans on writing in the rendered file

  - image: if your file is an image, you will find a PIL image object here
  - template: the tamplate used to render this page

  - meta:
    - modular: a list of subpages, if your page is modular
    - ...: all page specific yaml configuation, as well as global variables from metadata.yaml
```

[< back](README.md)
