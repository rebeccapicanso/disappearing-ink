#!/bin/sh

if [ $# -ne 1 ]; then
  echo "Usage: $0 filename"
  exit 1
fi

if [ ! -f $1 ]; then
  echo "File $1 not found."
  exit 2
fi

cat /dev/urandom | head -c $(stat -c %s $1) > $1

cat /dev/urandom | head -c $(stat -c %s $1) > $1

cat /dev/urandom | head -c $(stat -c %s $1) > $1

mv $1 $1.corrupt

cat $1.corrupt | head -c $(stat -c %s $1.corrupt) > $1

echo "File $1 has been corrupted and saved as $1.corrupt"
exit 0
```
