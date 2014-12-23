replayer
========

Replay easily Apache access.logs.

Installation
------------

`pip install replayer`

Usage
-----

Here is an example configuration file:

```
[General]
Host = localhost
LogFormat =

[Filter]
Methods =
Status =

[Header]
User-agent = Fancy testing with replayer
Host = www.yourserver.de

[Transform]
search =
replace =
```