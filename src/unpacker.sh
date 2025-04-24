# This runs on the transmission server

for rar in `find $TR_TORRENT_DIR -name "*.rar"; find $TR_TORRENT_DIR -name "*.zip"`; do
unrar $rar
done

for pkg in `find $TR_TORRENT_DIR -name "*.pkg"`; do
mv $pkg /ps4
done
