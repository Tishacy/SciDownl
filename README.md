<h1>SciDownl</h1>

An unofficial api for downloading papers from SciHub.

- Support downloading with DOI or PMID.
- Easy to update newest SciHub domains.
- Ready for changes: Encapsulate possible future changes of SciHub as configurations.
- Support proxies.

# Quick Usage

```bash
# Download with a DOI and filenmae is the paper's title.
$ scidownl download --doi https://doi.org/10.1145/3375633

# Download with a PMID and a user-defined filepath
$ scidownl download --pmid 31395057 --out ./paper/paper-1.pdf

# Download with a proxy: SCHEME=PROXY_ADDRESS 
$ scidownl download --pmid 31395057 --out ./paper/paper-1.pdf --proxy http=socks5://127.0.0.1:7890
```

# Installation

## Install with pip

Scidownl could be easily install with pip.

```bash
$ pip3 install -U scidownl
```

## Install from source code

```bash
$ git clone https://github.com/Tishacy/SciDownl.git
$ cd Scidownl && python3 setup.py install
```

# Usage

## Command line tool

```bash
$ scidownl -h
Usage: scidownl [OPTIONS] COMMAND [ARGS]...

  Command line tool to download pdfs from Scihub.

Options:
  -h, --help  Show this message and exit.

Commands:
  config         Get global configs.
  domain.list    List available SciHub domains in local db.
  domain.update  Update available SciHub domains and save them to local db.
  download       Download paper(s) by DOI or PMID.
```

### 1. Update available SciHub domains

```bash
$ scidownl domain.update --help
Usage: scidownl domain.update [OPTIONS]

  Update available SciHub domains and save them to local db.

Options:
  -m, --mode TEXT  update mode, could be 'crawl' or 'search', default mode is
                   'crawl'.
  -h, --help       Show this message and exit.
```

There are 2 update modes that you could specify with an option: `-m` or `--mode`

-   `crawl`: [Default] Crawling the real-time updated SciHub domains website (aka, SciHub domain source) to get available SciHub domains. The SciHub domain source website url is configured in the global config file in the section `[scihub.domain.updater.crawl]` with the key of `scihub_domain_source`. You could use `scidownl config --location` to show the location of the global config file and edit it.

    ```ini
    ; Global config file: global.ini
    ; ...
    [scihub.domain.updater.crawl]
    scihub_domain_source = http://tool.yovisun.com/scihub
    ; ...
    ```

	An example of using `crawl` mode:

    ```bash
    $ scidownl domain.update --mode crawl
    [INFO] | 2022/03/07 21:07:50 | Found 6 valid SciHub domains in total: ['http://sci-hub.ru', 'http://sci-hub.se', 'https://sci-hub.ru', 'https://sci-hub.st', 'http://sci-hub.st', 'https://sci-hub.se']
    [INFO] | 2022/03/07 21:07:50 | Saved 6 SciHub domains to local db.
    ```

-   `search`：Generate combinations according to the rules of SciHub domains and search for available SciHub domains. This will take longer than `crawl` mode.

	An example of using `search` mode:

    ```bash
    $ scidownl domain.update --mode search
    [INFO] | 2022/03/07 21:08:44 | # Search valid SciHub domains from 1352 urls
    [INFO] | 2022/03/07 21:08:48 | # Found a SciHub domain url: https://sci-hub.ru
    [INFO] | 2022/03/07 21:08:48 | # Found a SciHub domain url: https://sci-hub.st
    ...
    [INFO] | 2022/03/07 21:09:04 | Found 6 valid SciHub domains in total: ['https://sci-hub.ru', 'https://sci-hub.st', ...]
    [INFO] | 2022/03/07 21:09:04 | Saved 6 SciHub domains to local db.
    ```

### 2. List all saved SciHub domains

SciDownl use [SQLite](https://www.sqlite.org/) as the local database to store all updated SciHub domains locally. You can list all saved SciHub domains with the command `domain.list`.

```bash
$ scidownl domain.list
+--------------------+----------------+---------------+
| Url                |   SuccessTimes |   FailedTimes |
|--------------------+----------------+---------------|
| http://sci-hub.ru  |              0 |             0 |
| https://sci-hub.ru |              0 |             0 |
| https://sci-hub.st |              0 |             0 |
| http://sci-hub.st  |              0 |             0 |
| https://sci-hub.se |              0 |             0 |
| http://sci-hub.se  |              0 |             0 |
+--------------------+----------------+---------------+
```

In addition to the easy-to-understand Url column, the `SuccessTimes` column is used to record the number of successful paper downloads using this Url, and the `FailedTimes` column is used to record the number of failed paper downloads using this Url. These two columns are used to calculate the priority of choosing a SciHub domain when downloading papers.

### 3. Download papers

```
$ scidownl download --help
Usage: scidownl download [OPTIONS]

  Download paper(s) by DOI or PMID.

Options:
  -d, --doi TEXT         DOI string. Specifying multiple DOIs is supported,
                         e.g., --doi FIRST_DOI --doi SECOND_DOI ...
  -p, --pmid INTEGER     PMID numbers. Specifying multiple PMIDs is supported,
                         e.g., --pmid FIRST_PMID --pmid SECOND_PMID ...
  -o, --out TEXT         Output directory or file path, which could be an
                         absolute path or a relative path. Output directory
                         examples: /absolute/path/to/download/,
                         ./relative/path/to/download/, Output file examples:
                         /absolute/dir/paper.pdf, ../relative/dir/paper.pdf.
                         If --out is not specified, paper will be downloaded
                         to the current directory with the file name of the
                         paper's title. If multiple DOIs or multiple PMIDs are
                         provided, the --out option is always considered as
                         the output directory, rather than the output file
                         path.
  -u, --scihub-url TEXT  Scihub domain url. If not specified, automatically
                         choose one from local saved domains. It's recommended
                         to leave this option empty.
  -h, --help             Show this message and exit.
```

#### Download papers with DOI(s) or PMID(s)

Using option `-d` or `--doi` to download papers with DOI, and option `-p` or `--pmid` to download papers with PMID. You can specify these options for multiple times, and even mix of them.

```bash
# with a single DOI
$ scidownl download --doi https://doi.org/10.1145/3375633

# with multiple DOIs
$ scidownl download --doi https://doi.org/10.1145/3375633 --doi https://doi.org/10.1145/2785956.2787496

# with a single PMID
$ scidownl download --pmid 31395057

# with multiple PMIDs
$ scidownl download --pmid 31395057 --pmid 24686414

# with a mix of DOIs and PMIDs
$ scidownl download --doi https://doi.org/10.1145/3375633 --pmid 31395057 --pmid 24686414
```

#### Customize the output location of papers

By default, the downloaded paper is named by the paper's title. With option `-o` or `--out`，you can customize the output location of downloaded papers, whcih could be an absolute path or a relative path, and a direcotry or a file path.

-   Output the paepr to a directory:

    ```bash
    $ scidownl download --pmid 31395057 --out /absolute/path/of/a/directory/
    # NOTE that the '/' at the end of the directory path is required, otherwise the last segment will be treated as the filename rather than a directory.
    
    $ scidownl download --pmid 31395057 --out ../relative/path/of/a/directory/
    # The '/' at the end of the directory path is required too.
    ```

-   Output the paper with the file path.

    ```bash
    $ scidownl download --pmid 31395057 --out /absolute/dir/paper.pdf
    $ scidownl download --pmid 31395057 --out ../relative/dir/paper.pdf
    $ scidownl download --pmid 31395057 --out relative/dir/paper.pdf
    $ scidownl download --pmid 31395057 --out paper  # will be downlaoded as ./paper.pdf
    ```

**NOTE** that if there are more than one papers to be downloaded, the value of the `--out` option will always be considered as a directory, rather than a file path.

```bash
$ scidownl download --pmid 31395057 --pmid 24686414 --out paper
# will be downloaded to ./paper/ directory:
#  ./paper/<paper-title-1>.pdf
#  ./paper/<paper-title-2>.pdf
```

If some directories in the option are not exist, SciDownl will create them for you :smile:.

#### Use a specific SciHub url

With option `-u` or `--scihub-url`, you could use a specific SciHub url you want, rather than let SciDownl automatically choose one for you from local saved SciHub domains. It's recommended to let SciDownl choose a SciHub url, so you don't need to use this option in normal use.

```bash
$ scidownl download --pmid 31395057 --scihub-url http://sci-hub.se
```

## Module use

You could use `scihub_download` function to download papers.

```python
from scidownl import scihub_download

paper = "https://doi.org/10.1145/3375633"
paper_type = "doi"
out = "./paper/one_paper.pdf"
proxies = {
    'http': 'socks5://127.0.0.1:7890'
}
scihub_download(paper, paper_type=paper_type, out=out, proxies=proxies)
```

More examples could be seen in [examples](./example/simple.py).

# LICENSE

Copyright (c) 2022 tishacy.

Licensed under the [MIT License](https://github.com/Tishacy/SciDownl/blob/v1.0/LICENSE).
