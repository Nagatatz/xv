#!/bin/sh
# https://qiita.com/shiena/items/47437f4f7874bf70d664

set -e

host="$1"
shift
user="$1"
shift
password="$1"
shift

echo "Waiting for mysql"
until mysql -h"$host" -u"$user" -p"$password" &> /dev/null
do
        >$2 echo -n "."
        sleep 1
done

>&2 echo "MySQL is up - executing command"