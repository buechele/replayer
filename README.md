# replayer

Replay easily an Apache access.log.

## Installation

`pip install replayer`

or

`easy_install replayer`

## Usage

Here is an example configuration file:

```
[General]
Host = localhost
LogFormat = %h %l %u %t \"%r\" %>s %b

[Filter]
Rule = allow
Methods = GET
Status = 200

[Header]
User-Agent = Lynx/2.8.4rel.1 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.6c
Host = www.yourserver.de

[Transform]
search = \;jsessionid=[^?]+
replace =
```

#### Section `General`

| Entry     | Description |
|-----------|-------------|
| Host      | The host to which the requests will be send. |
| LogFormat | The format of the Apache access.log. |

#### Section `Filter`

Requests will only take place, if all configured criteria are satisfied for the original request in the Apache access.log.

| Entry     | Description |
|-----------|-------------|
| Rule      | `allow` or `disallow` requests from access.log. Defaults to `allow`. |
| Methods   | HTTP methods which are (dis)allowed. |
| Status    | Status codes which are (dis)allowed. |

#### Section `Header`

User-defined headers which will be part of the request header.

#### Section `Transform`

Gives the ability to manipulate the URL before the request will take place. The section has to start with the string
`Transform`, so it is possible to define multiple `Transform` sections (e.g. `Transform_remove_jsession` will be also a
valid `Transform` section).

| Entry   | Description |
|---------|-------------|
| Search  | String to search in request URL. Regular expressions are allowed. |
| Replace | Replacement for Strings which were found. |

## See also

* [Apache Module mod_log_config](http://httpd.apache.org/docs/2.4/mod/mod_log_config.html)