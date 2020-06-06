wget -w 2 -m 'http://www.gutenberg.org/robot/harvest?filetypes[]=txt&langs[]=en'

for file in (cat www.gutenberg.org/robot/harves* | pup 'a json{}' | jq -r '.[].href | sel
ect(. | endswith(".zip"))')
    wget $file
end

python agg.py
