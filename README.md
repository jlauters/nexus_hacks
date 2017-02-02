# Nexus Hacks

dumping ground for nexus file manipulation scripts

- XLSX -> NEXUS conversion script ( no character names )
- TXT -> NEXUS conversion script
- Repair bad NEXUS dimension values
- Verifies Taxonomy names through GNParser


# to run:

morpho_xlsx_no_chars.py takes a filepath as argument,
it tries to infer the file type and sends to an appropriate matrixHandler.
MatrixHandlers call a readfile method on init that handles the bulk of functionality.

```
$ python morpho_xlsx_no_chars.py {path/to/file}
```


