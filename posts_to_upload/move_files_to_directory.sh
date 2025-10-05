#!/bin/bash
BASE=~/projects/spherevista360/posts_to_upload
# Extract category from YAML and move the file into a same-named folder
# (assumes first "category:" in file is the right one)
find "$BASE" -maxdepth 1 -type f -name '*.md' -print0 | while IFS= read -r -d '' f; do
  catname=$(grep -m1 '^category:' "$f" | sed 's/category:\s*"\{0,1\}\([^"]*\)"\{0,1\}/\1/i')
  catname=${catname:-Unsorted}
  mkdir -p "$BASE/$catname"
  mv "$f" "$BASE/$catname/"
done
