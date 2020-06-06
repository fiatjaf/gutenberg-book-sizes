deploy: index.html data.json.br
	rsync index.html data.json.br nusakan-58:gutenberg/

data.json.br: books/data
	jq --slurp -c 'map(.id = (.id | split("-") | .[0])) | unique_by(.id) | sort_by(.characters) | map([.author, .id, .title, .characters, .letters, .words])' books/data > data.json
	brotli -c data.json > data.json.br
