from transmission_rpc import Client
from os import getenv
import logging

client = Client(host=getenv("transmission_host"))
torrents = client.get_torrents(arguments=["trackers", "name", "status"])

## statuses:
# STOPPED = 'stopped'
# CHECK_PENDING = 'check pending'
# CHECKING = 'checking'
# DOWNLOAD_PENDING = 'download pending'
# DOWNLOADING = 'downloading'
# SEED_PENDING = 'seed pending'
# SEEDING = 'seeding'

special_trackers = set(getenv("special_trackers").split(","))
logging.info(f"Special trackers:\n{'\n'.join(special_trackers)}\n")

logging.info(f"===Session settings:\n{client.get_session()}\n===\n")

for torrent in torrents:
    special = False
    trackers = {x.announce.split("/")[2] for x in torrent.trackers} # just hostnames
    special = (special_trackers & trackers)
    if special:
        client.change_torrent(torrent.info_hash, seed_ratio_mode="unlimited", labels=special)
        if len(trackers) > 1:
            logging.warning(f"there is more than one tracker for special torrent {torrent.name}: {trackers}")
    if not special:
        client.change_torrent(torrent.info_hash, seed_ratio_limit=0.01)
        if torrent.status in ["seeding", "seed pending"]:
            client.stop_torrent(torrent.info_hash)
            logging.info(f"Stopped torrent {torrent.name}")
