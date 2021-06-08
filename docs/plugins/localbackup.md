# Local Backup

Type: `backup`  
Enabled by default: `false`

Keeps a limited number of project copies on your local machine.

**Please use the Git plugin for actual backups!**

Restoring a backup is a manual task.

---

|argument				|default value		|explanation										|
|-----------------------|-------------------|---------------------------------------------------|
|PRIORITY				|30					|													|
|MAX					|10					|number of backups kept before deleting the oldest	|
|BAKROOT				|[next to devroot]	|													|
