# SciDownl

Download pdfs from Scihub via DOI.
- Easy to use.
- Captcha is done.

## Install
*PyPI is on the way.*

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
#### Example
```bash
# download to the current directory
$ scidownl -D 10.1021/ol9910114
$ scidownl -D 10.1021/ol9910114 -o .

# download to the specified directory
$ scidownl -D 10.1021/ol9910114 -o paper

# update available links of Scihub
$ scidownl -u
[INFO] Updating links ...
[INFO] http://sci-hub.fun
[INFO] https://sci-hub.fun
[INFO] http://sci-hub.se
[INFO] http://sci-hub.tw
[INFO] http://sci-hub.run
[INFO] https://sci-hub.se
[INFO] https://sci-hub.tw
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

## LICENSE

Copyright (c) 2019 tishacy.

Licensed under the [MIT License](./LICENSE).
