Tarsnap Prune
=============

This script will read the list of archives from the tarsnap servers.  It will then give you the
option to delete the archives that are older than the cutoff date (90 days ago by default).

Usage
-----

```shell
$ tarsnap-prune prune
INFO: Keeping 89 archives
INFO: Deleting 384 archives from 2017-02-21 to 2018-03-09
Delete archives?  ("yes" proceeds, anything else aborts):
```
Then follow the prompts.

### Cutoff Date

By default the script keeps 90 days of archives.  You can override that default:

```shell
$ ./tarsnap-prune prune 30
```

### List Archives Cache

By default the command caches the tarsnap `list-archives` output based on the current date (since
that command can take awhile to run).  You can use `--ignore-cache` to override this behavior.


Development
-----------

* Intended to be distributed as a shiv-built pyz.  Use `shiv/build` to create one.
* Can use `scripts/rsync-pyz` to watch for changes to files that would affect the .pyz, build it,
    and rsync it to a server: `./scripts/rsync-pyz circus /home/rsyring/bin`
* Once it's working well on a server, "install" with:
    `sudo mv tarsnap-prune.pyz /usr/local/bin/tarsnap-prune`
