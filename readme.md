Tarsnap Prune
=============

This script will read the list of archives from the tarsnap servers.  It will then give you the
option to delete the archives that are older than the cutoff date (90 days ago by default).

Usage
-----

```shell
$ ./tarsnap-prune prune
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

By default the command caches the tarsnap `list-archives` output based on the current date (since that
command can take awhile to run).  You can use `--ignore-cache` to override this behavior.


Install
-------

```
$ ssh -A server
$ sudo -E git clone git@github.com:level12/tarsnap-prune.git /opt/tarsnap-prune-src
$ sudo -i
# virtualenv /opt/tarsnap-prune-venv
# . /opt/tarsnap-prune-venv/bin/activate
# cd /opt/tarsnap-prune-src/
# pipenv install

Fsck
-----

You may get errors when trying to delete an archive:

```
plumbum.commands.processes.ProcessExecutionError: Command line: ['/usr/bin/tarsnap', '--cachedir', '/tmp/tarsnap-cache', '--keyfile', '/tmp/server-name-tarsnap.key', '-d', '-f', 'scooby_daily_backup_scooby_20170221-150108']
Exit code: 1
Stderr:  | tarsnap: Sequence number mismatch: Run --fsck
         | tarsnap: Error deleting archive
         | tarsnap: Error exit delayed from previous errors.
```

In that case, it's probably easiest to run the fsck from the server, although you could run it
locally if you wanted.

```
rsyring@loftey$ ssh scooby
rsyring@scooby$ sudo tarsnap --fsck
```
