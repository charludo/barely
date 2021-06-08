# SFTP

Type: `publication`  
Enabled by default: `false`

Uploads your webroot to an SFTP Webserver after you have exited barely.

Works with either a username/password, or an SSH key.

---

|argument				|default value		|explanation																		|
|-----------------------|-------------------|-----------------------------------------------------------------------------------|
|PRIORITY				|90					|																					|
|HOSTNAME				|					|																					|
|username				|					|																					|
|PASSWORD				|					|																					|
|KEY					|					|if a key is specified, it will be preferred over a password						|
|ROOT					|					|dir for the files on the server. check with your host for a correct absolute path!	|
