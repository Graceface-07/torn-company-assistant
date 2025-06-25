#!/bin/bash

DOCS_DIR="./docs"
YML_FILE="mkdocs.yml"
BACKUP_FILE="mkdocs.yml.bak"

cp "$YML_FILE" "$BACKUP_FILE"

awk '
  /^[[:space:]]*-[[:space:]]/ && /\.md/ {
    match($0, /[^:]*:[[:space:]]*([a-zA-Z0-9_\/\-\.]+\.md)/, arr)
    if (arr[1] != "") {
      md[arr[1]] = $0
    }
  }
  { lines[NR] = $0 }
  END {
    for (i = 1; i <= NR; i++) {
      printed = 0
      for (f in md) {
        if (lines[i] == md[f]) {
          if (!system("[ -f \"" ENVIRON["DOCS_DIR"] "/" f "\" ]")) {
            print lines[i]
          } else {
            print "# ⛔ Missing file, commented out:"
            print "# " lines[i]
          }
          printed = 1
        }
      }
      if (!printed)
        print lines[i]
    }
  }
' "$YML_FILE" > "$YML_FILE.tmp"

mv "$YML_FILE.tmp" "$YML_FILE"
echo "✅ Done: missing .md entries commented in $YML_FILE (original backed up to $BACKUP_FILE)"
