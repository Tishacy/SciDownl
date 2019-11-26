# SciDownl

Download pdfs from Scihub via DOI.
- Easy to use.
- Easy to deal with captcha.
- Easy to update Scihub newest domains.

<img src="./demo.svg">

## Install
```bash
$ pip3 install -U scidownl
```

## Usage
### Command line
```bash
$ scidownl -h
usage: Command line tool to download pdf via DOI from Scihub.
       [-h] [-c CHOOSE] [-D DOI] [-o OUTPUT] [-u] [-l]

optional arguments:
  -h, --help            show this help message and exit
  -c CHOOSE, --choose CHOOSE
                        choose scihub url by index
  -D DOI, --DOI DOI     the DOI number of the paper
  -o OUTPUT, --output OUTPUT
                        directory to download the pdf
  -u, --update          update available Scihub links
  -l, --list            list current saved sichub urls
```
#### Examples
```bash
# Update available links of Scihub
$ scidownl -u
[INFO] Updating links ...
[INFO] https://sci-hub.ren
[INFO] http://sci-hub.ren
[INFO] http://sci-hub.red
[INFO] http://sci-hub.se
[INFO] https://sci-hub.se
[INFO] http://sci-hub.tw

# Choose scihub url by the index.
$ scidownl -c 5
Current scihub url: http://sci-hub.tw

# List available links of Scihub. You can see the current scihub url is pointing to the 5th scihub url.
$ scidownl -l
  [0] https://sci-hub.ren
  [1] http://sci-hub.ren
  [2] http://sci-hub.red
  [3] http://sci-hub.se
  [4] https://sci-hub.se
* [5] http://sci-hub.tw

# Download to the current directory
$ scidownl -D 10.1021/ol9910114
$ scidownl -D 10.1021/ol9910114 -o .

# Download to the specified directory, ie. '-o paper' for downloading to paper directory.
$ scidownl -D 10.1021/ol9910114 -o paper

# if 'PermessionError' shows, just use sudo. ie:
$ sudo scidownl -u
```

### Module

If you have a list of DOIs, using `scidownl` in your python scripts for downloading all of the papers is recommended.

Download single paper via DOI.
```python
from scidownl.scihub import *

DOI = "10.1021/ol9910114"
out = 'paper'
sci = SciHub(DOI, out).download(choose_scihub_url_index=3)
```

Dowloading a list of DOIS by simply using a for loop.
```python
from scidownl.scihub import *

DOIS = [...]
out = 'paper'
for doi in DOIS:
  SciHub(doi, out).download(choose_scihub_url_index=3)
```

Update available Scihub links.
```python
from scidownl.update_link import *

# Use crawling method to update available Scihub links.
update_link(mod='c')
# Use brute force search method to update available Scihub links.
update_link(mod='b')
```
## RELEASE
- v0.1.0: First release.
- v0.2.0:
  - Optimized the download speed.
  - Optimized the captcha processment.
- v0.2.1:
  - Applied stream download.
  - Display of download progress is added.
  - Fixed bugs of invalid scihub links.
- v0.2.2:
  - Add new source website.
  - Add `-l/--list` argument in command line tool.
- v0.2.3:
  - Fix bugs of empty filename and wrong scidhub urls.
  - Fix bugs in the brute-force method of updating scihub urls.
- V0.2.4:
  - Fix #2.
  - Fix bugs of error: file name too long.
- V0.2.5:
  - Reconstruct code.
  - Fix 'no content-length' error.
  - Add `-c/--choose` argument for manually choosing scihub url used.
- V0.2.6:
  - Fix bug where retry time too long.

## LICENSE

Copyright (c) 2019 tishacy.

Licensed under the [MIT License](./LICENSE).
