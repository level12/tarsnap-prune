#!/usr/bin/env python

from collections import namedtuple
import datetime as dt
import logging
from pathlib import Path

import arrow
import click
from plumbum.cmd import tarsnap

log = logging.getLogger(__name__)

ToDelete = namedtuple('ToDelete', 'keep delete first_date last_date names')


@click.group()
def main():
    log_format = '%(levelname)s: %(message)s'
    logging.basicConfig(format=log_format, level=logging.INFO)


@main.command()
@click.argument('keep_days', default=90)
@click.option('--ignore-cache', is_flag=True, default=False)
def prune(ignore_cache, keep_days):
    log_format = '%(levelname)s: %(message)s'
    logging.basicConfig(format=log_format, level=logging.INFO)

    ts = dt.date.today()
    cache_fname = 'tarsnap-prune.{}'.format(ts)

    cache_fpath = Path('/tmp/{}'.format(cache_fname))

    if ignore_cache or not cache_fpath.exists():
        log.info('Getting archives from tarsnap servers...')
        (tarsnap['--list-archives'] > str(cache_fpath))()

    with cache_fpath.open() as fo:
        lines = fo.read().splitlines()
    to_delete = to_delete_archives(lines, keep_days)

    log.info('Keeping {.keep} archives'.format(to_delete))
    log.info('Deleting {0.delete} archives from {0.first_date} to {0.last_date}'.format(to_delete))
    proceed = input('Delete archives?  ("yes" proceeds, anything else aborts): ')
    if proceed != 'yes':
        log.info('Aborting')
        return

    log.info('Deleting archives...')
    for archive_name in to_delete.names:
        result = tarsnap(key_fpath, '-d', '-f', archive_name)
        print(result)
        return


def date_name_pair(archive_name):
    # Like scooby_daily_backup_scooby_20180514-031301
    parts = archive_name.split('_')
    # Like 20180514-031301
    date, time = parts.pop().split('-')
    return arrow.get(date, 'YYYYMMDD'), archive_name


def to_delete_archives(archive_names, keep_days):
    date_name_pairs = [date_name_pair(name) for name in sorted(archive_names)]
    cutoff_date = arrow.get().shift(days=keep_days * -1)

    to_delete = [(date, name) for date, name in date_name_pairs
                 if date < cutoff_date]

    first_date = to_delete[0][0].date().isoformat()
    last_date = to_delete[-1][0].date().isoformat()
    delete_count = len(to_delete)
    keep_count = len(archive_names) - delete_count
    return ToDelete(keep_count, delete_count, first_date, last_date,
                    [name for date, name in to_delete])


if __name__ == '__main__':
    main()
