#!/usr/bin/env bash
set -ex
new="$1"
shift
if [ $# -gt 0 ]; then
  old="$1"
  shift
else
  old='Min'
fi


old="$(echo "$old" | sed -E 's/\/$//')"
new="$(echo "$new" | sed -E 's/\/$//')"
old_base=$(basename $old)
new_base=$(basename $new)
echo $old_base
cp -r "$old" "$new"
cd "$new"
old_lower="$(echo "$old_base" | tr 'A-Z' 'a-z')"
new_lower="$(echo "$new_base" | tr 'A-Z' 'a-z')"
find . -type f -print0 | xargs -0 sed -i "s/${old_base}/${new_base}/g"
find . -type f -print0 | xargs -0 sed -i "s/${old_lower}/${new_lower}/g"
rename "s/${old_base}/${new_base}/" *.iml
rename "s/${old_lower}/${new_lower}/" *.iml
cd app/src/test/java/com/example/remaui/
mv ${old_lower} ${new_lower}
cd "$new"
cd app/src/main/java/com/example/remaui/
mv ${old_lower} ${new_lower}
cd "$new"
cd app/src/androidTest/java/com/example/remaui/
mv ${old_lower} ${new_lower}
