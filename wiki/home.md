# barely CMS

barely CMS aims to be a minimal CMS, allowing a user the rapid development and deployment of static (or mostly static) websites. Flatfiles are utilized instead of a traditional database for ease of access and portability. Importantly, style and content are strictly separated by use of a themeing and templating engine. barely will run as a standalone python CLI application and should run on Linux, Windows, and Mac. With it, rapid development of customer websites should be possible.

To start with a new project, users will be able to leverage build-in templates for a uick start. Alternatively, users can also create the necessary files and directories by hand, and integrate barely at a later point.
To use barely, the user will have two possibilitites. Either they can make the desired changes to style, stucture or content of the site first, then call on barely to translate those changes to a static website; or they can start barely in live mode, whereupon a rudimentary webserver is started in the background, and changes to the template files, assets and content will immediately be mirrored on that webserver, to further aid in the rapid development process. To achieve this, barely will track any changes to the development directory and upon update, creation or deletion of files or directories only update those parts of the project that are tangiated by the changes in the static translation.

Upon finishing the desired changes, the user will have the option to push the changes to an sftp server. The reason for this is that barely aims to not only offer the capability of generating static websites, but also to place them exactly where they are needed - be it on a webserver the user manages, for example in a directory that is being pointed to by a reverse proxy, or on a managed server on which the user is not allowed to execute programs like barely. In the former case, barely should offerto symlink the static output directory to a convenient location.

barely wants to keep development processes as simple as possible, and this includes its configuration. barely knows three types of config files:
- config.yaml, placed in the root of the development folder, contains global configurations (eg. what filetypes to render or compress, where the output directory is located, etc)
- metadata.yaml, placed alongside config.yaml, contains global metadata info for the website (eg. common tags, titles, languages)
- inside each renderable file, the user is able to specify additional yaml, which can override global parameteres or create new ones to be used in just that file

Alongside the mentioned config files, a folder "templates" must be situated. In it, all templates and partial templates must be stored, though organization by means of naming conventions and subdirectory structures is left up to the user. The global config files, plus the files in this templates-directory are the only ones that barely will not try to translate into static files and put them in the specified devroot. During live development, these still need be monitored for changes, of course, and if changes occur, all content that utilizes either a changes template, or any template inheriting from it, needs to be re-translated.

Special attention also needs to be placed on ressource files. Changes to a ressource (be it an image, css, or a script) can have effects on many content pages. A change to a css file that is linked inside a base template would, for example, necessitate the re-render of every single page that in some form utilizes the base template, or any descendant of that template. To ease the strain on barely during such procedures, the decision has been made that changes to ressource files placed somewhere in the optional "res" directory will be tracked and cascaded through any file it affects, while changes to ressources placed alongside content files ("local ressources") will only be checked against that specific content file.

As a convenience to the user, two types of pages are understood by barely: regular pages, consisting of exactly one content file and a utilized template, and modular pages, which utilize a template, and include any number of ordered sub-content-pages, each with their own utilized template.
Regular pages, modular parent pages and modular child pages all signify their utilized template by using that templates name as their filename. The path to a page (not including its filename) is equivalent to the path in a browser to change the rendered translation of that page. Modular child pages however live in folders starting with an underscore; these folders are ignored in the rendering process, except when changes to them or their contents trigger a re-render of their parent page. The parent page, on the other hand, has to specify in yaml the order and names of the child pages that should be included during rendering.

The same notation also opens the possibility of collections, meaning the grouping of pages based on certain attributes, like yaml category tags. This enables behavior that appears dynamic even on static websites, at least in a limited way.

Furthermore, users should be able to utilize plugins. barely will provide hooks at selected points in the program to allow user plugins to further menipulate the static output. One of the standard plugins that will come preinstalled with barely is the aforementioned sftp solution; another one would be a rudimentary collections plugin; also a forms plugin that renders yaml to HTML forms via a template, and provides customizable options for email sending.

Lastly a backup and restore functionality is included in barely. It is not meant as a replacement for, e.g., a version management software, but can still help in preventing data loss or rolling back unwanted changes.