mkdir "/usr/bin/prekladac"
cp -r "src" "/usr/bin/prekladac/"
cp -r "config" "/usr/bin/prekladac/"
mkdir "/usr/bin/prekladac/logs"
touch "/usr/bin/prekladac/logs/log.txt"
chmod ugo+w "/usr/bin/prekladac/logs/log.txt"
cp "prekladac.service" "/etc/systemd/system/prekladac.service"