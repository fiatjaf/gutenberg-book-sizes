The result of downloading all books in English from Gutenberg Project and counting their words, characters, letters (not spaces) and presenting them in a sorted table.

To reproduce, run the following:

```
cd books
fish fetchdata.fish
cd ..
make
```

This will give you the files `data.json` and `data.json.br` (brotli-compressed because otherwise it would be too big, if you don't have brotli installed it will fail but you can still use `data.json` directly), to load the non-brotli version from `index.html` change the extension there.

This uses [sifter](https://www.npmjs.com/package/sifter) and [clusterize](https://clusterize.js.org/) and is being served on https://alhur.es/books/ with [Caddy](https://caddyserver.com/) and the following `Caddyfile` snippet (very hacky way of serving brotli stuff):

```
alhur.es {
  handle /books/* {
    uri strip_prefix /books
    root * /home/fiatjaf/directory-where-index-and-data-json-are
    header /**/*.br Content-Encoding br
    header /**/*.json.br Content-Type application/json
    file_server
  }

  ...other stuff
}
```
