# SciDownl

Download pdfs from Scihub via DOI.
- Easy to use.
- Easy to deal with captcha.
- Easy to update Scihub newest domains.

## Install
```bash
pip3 install scidownl
```

## Usage
### Command line
```bash
$ scidownl -h
usage: Command line tool to download pdf via DOI from Scihub.
       [-h] [-D DOI] [-o OUTPUT] [-u]

optional arguments:
  -h, --help            show this help message and exit
  -D DOI, --DOI DOI     the DOI number of the paper
  -o OUTPUT, --output OUTPUT
                        directory to download the pdf
  -u, --update          update available Scihub links
```
#### Examples
```bash
# download to the current directory
$ scidownl -D 10.1021/ol9910114
$ scidownl -D 10.1021/ol9910114 -o .

# download to the specified directory
$ scidownl -D 10.1021/ol9910114 -o paper

# update available links of Scihub
$ scidownl -u
[INFO] Updating links ...
[INFO] http://sci-hub.se
[INFO] http://sci-hub.tw
[INFO] https://sci-hub.se
[INFO] https://sci-hub.tw

# if show 'PermessionError' when updating, just use sudo.
$ sudo scidownl -u
```
### Module
Download a paper via DOI.
```python
from scidownl.scihub import *

DOI = "10.1021/ol9910114"
out = 'paper'
sci = SciHub(DOI, out)
sci.download()
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

## LICENSE

Copyright (c) 2019 tishacy.

Licensed under the [MIT License](./LICENSE).
