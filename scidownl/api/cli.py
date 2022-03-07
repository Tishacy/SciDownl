# -*- coding: utf-8 -*-
"""Command line tool of scidownl."""
import os.path

import click

from ..log import get_logger

logger = get_logger()


@click.group()
@click.help_option("-h", "--help")
def cli():
    """Command line tool to download pdfs from Scihub."""
    pass


@cli.command("config")
@click.option("-l", "--location", is_flag=True, help="Show the location of global config file.")
@click.option("-g", "--get", type=(str, str), help="Get config by section and key, "
                                                   "usage: --get <section> <key>.")
@click.help_option("-h", "--help")
def config(location, get):
    """Get global configs."""
    from ..config import get_config, GlobalConfig

    configs = get_config()
    if location:
        logger.info(f"Global config file path: {GlobalConfig.config_fpath}")
        return

    if get:
        sec, key = get
        if sec not in configs.sections():
            logger.warning(f"Section '{sec}' is not found. Valid sections: {configs.sections()}")
            return
        value = configs[sec].get(key, None)
        if value is None:
            logger.warning(f"Key '{key} is not found. Valid keys: {list(dict(configs.items(sec)).keys())}")
            return
        logger.info(f"Value: {configs[sec][key]}")


@cli.command("domain.update")
@click.option("-m", "--mode", default='crawl', help="update mode, could be 'crawl' or 'search',"
                                                    " default mode is 'crawl'.")
@click.help_option("-h", "--help")
def update_domains(mode):
    """Update available SciHub domains and save them to local db."""
    from ..core.updater import scihub_domain_updaters

    updater_cls = scihub_domain_updaters.get(mode, None)
    if updater_cls is None:
        logger.error(f"Update mode (-m) must be one of "
                     f"{list(scihub_domain_updaters.keys())}, got "
                     f"'{mode}' instead.")
        return
    updater = updater_cls()
    updater.update_domains()


@cli.command("domain.list")
@click.help_option("-h", "--help")
def list_domains():
    """List available SciHub domains in local db."""
    import tablib
    from ..db.service import ScihubUrlService

    service = ScihubUrlService()
    urls = service.get_all_urls()
    urls.sort(key=lambda url: url.success_times, reverse=True)
    tab = tablib.Dataset(headers=["Url", "SuccessTimes", "FailedTimes"])
    for url in urls:
        tab.append((url.url, url.success_times, url.failed_times))
    tab_str = tab.export("cli", tablefmt="psql")
    print(tab_str)


@cli.command("download")
@click.option("-d", "--doi", multiple=True,
              help="DOI string. Specifying multiple DOIs is supported, "
                    "e.g., --doi FIRST_DOI --doi SECOND_DOI ... ")
@click.option("-p", "--pmid", multiple=True, type=int,
              help="PMID numbers. Specifying multiple PMIDs is supported, "
                   "e.g., --pmid FIRST_PMID --pmid SECOND_PMID ...")
@click.option("-o", "--out",
              help="Output directory or file path, which could be an absolute path "
                   "or a relative path. "
                   "Output directory examples: /absolute/path/to/download/, ./relative/path/to/download/, "
                   "Output file examples: /absolute/dir/paper.pdf, ../relative/dir/paper.pdf. "
                   "If --out is not specified, paper will be downloaded to the current directory "
                   "with the file name of the paper's title. "
                   "If multiple DOIs or multiple PMIDs are provided, the --out option is always considered "
                   "as the output directory, rather than the output file path.")
@click.option("-u", "--scihub-url",
              help="Scihub domain url. If not specified, automatically choose one from local saved domains. "
                   "It's recommended to leave this option empty.")
@click.help_option("-h", "--help")
def download(doi, pmid, out, scihub_url):
    """Download paper(s) by DOI or PMID."""
    from ..core.task import ScihubTask
    from ..config import get_config

    configs = get_config()

    logger.info("Run scihub tasks. Tasks information: ")
    if len(doi) > 0:
        logger.info("%15s: %s" % ("DOI(s)", list(doi)))
    if len(pmid) > 0:
        logger.info("%15s: %s" % ("PMID(s)", list(pmid)))

    if out is None:
        logger.info("%15s: %s" % ("Output", os.path.abspath('./')))
    else:
        logger.info("%15s: %s" % ("Output", out))

    if scihub_url is None:
        logger.info("%15s: <auto.%s>" % ("SciHub Url", configs['scihub.task']['scihub_url_chooser_type']))
    else:
        logger.info("%15s: %s" % ("SciHub Url", scihub_url))

    # Always consider out as a directory if there are multiple DOIs and PMIDs.
    if len(doi) + len(pmid) > 1:
        if out is not None and out[-1] != "/":
            out = out + '/'

    tasks = []
    for doi_item in doi:
        tasks.append({
            'source_keyword': doi_item,
            'source_type': 'doi',
            'scihub_url': scihub_url,
            'out': out
        })
    for pmid_item in pmid:
        tasks.append({
            'source_keyword': pmid_item,
            'source_type': 'pmid',
            'scihub_url': scihub_url,
            'out': out
        })
    for task_kwargs in tasks:
        task = ScihubTask(**task_kwargs)
        try:
            task.run()
        except Exception as e:
            logger.error(f"final status: {task.context['status']}, error: {task.context['error']}")


if __name__ == '__main__':
    cli()
