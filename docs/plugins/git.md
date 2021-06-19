# Git

Type: `backup`  
Enabled by default: `false`

Pushes to a remote origin whenever you are done rebuilding / live editing (unless you answer barelys exit prompt wih "no" or "publish only").

**Note:** git has to be installed. On Windows, GitHub Desktop is **not** sufficient. Check with `git --version`.

**Note**: the repository and its origin have to already be initialized. This plugin can not do that for you.

---

|argument				|default value		|explanation									|
|-----------------------|-------------------|-----------------------------------------------|
|PRIORITY				|40					|												|
|MESSAGE				|barely auto commit	|gets appended with a timestamp					|
|REMOTE_NAME			|origin				|												|
