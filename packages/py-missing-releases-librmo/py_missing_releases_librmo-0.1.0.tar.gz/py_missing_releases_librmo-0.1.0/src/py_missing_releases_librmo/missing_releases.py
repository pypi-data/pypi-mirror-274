
import json
import os
import logging
from dataclasses import dataclass
from pathlib import Path
from music_brainz_api_micro import MusicBrainzAPI as MBAPI
from ._database import DB


@dataclass
class AlbumArtist():
    name: str
    mb_id: str


@dataclass
class Release():
    name: str
    artist: AlbumArtist
    mb_id: str
    url: str


class MissingReleases():

    librmo_config_dir: str = os.path.join(
        str(Path.home()), ".config/librmo")
    librmo_db_name: str = 'media.db'

    known_album_releases: list[Release]
    albumartists: list[AlbumArtist]
    full_album_releases: list[Release]
    missing_releases: list[Release]

    db: DB

    mb: MBAPI

    def _debug(self, message):
        logging.debug(message)

    def _insert_report(self):
        pass

    def _compare_releases(self):
        self.missing_releases = []
        full_releases = [i.mb_id for i in self.full_album_releases]
        self._debug(f"Got {len(full_releases)} total releases")
        known_releases = [i.mb_id for i in self.known_album_releases]
        self._debug(f"Got {len(known_releases)} acquired releases")
        missing_releases = list(set(full_releases).difference(known_releases))
        filtered_list = list(
            filter(lambda c: c.mb_id in missing_releases, self.full_album_releases))
        self.missing_releases = filtered_list
        # self._debug(self.missing_releases)

    def _query_album_releases(self):
        self.full_album_releases = []
        for a in self.albumartists:
            result = self.mb.get_releases_by_artist(a.mb_id)
            if result.error is True:
                continue
            artist = json.loads(result.response)
            if 'release-groups' not in artist:
                continue
            release_groups = artist['release-groups']
            for r in release_groups:
                if r['primary-type'] != 'Album':
                    continue
                if 'secondary-types' in r:
                    if 'Live' in r['secondary-types']:
                        continue
                    if 'Compilation' in r['secondary-types']:
                        continue
                    if 'Demo' in r['secondary-types']:
                        continue
                self.full_album_releases.append(
                    Release(name=r['title'], mb_id=r['id'], url='', artist=a))
        # self._debug(self.full_album_releases)

    def _get_albumartists(self):
        self.albumartists = []
        for a in self.known_album_releases:
            response = self.mb.get_release_group(a.mb_id)
            if response.error is True:
                continue
            release = json.loads(response.response)
            if 'artist-credit' not in release:
                continue
            artist = release['artist-credit'][0]
            exists = next(
                (x for x in self.albumartists if x.mb_id == artist['artist']['id']), None)
            if exists is not None:
                continue
            album_artist = AlbumArtist(
                name=artist['name'], mb_id=artist['artist']['id'])
            a.artist = album_artist
            self.albumartists.append(album_artist)
        # self._debug(self.albumartists)

    def _get_album_groups(self):
        self.known_album_releases = []
        album_groups = self.db.get_all_album_groups()
        for a in album_groups:
            self.known_album_releases.append(
                Release(name=a[1], mb_id=a[0], url='', artist=None))
        # self._debug(self.known_album_releases)

    def _connect_librmo(self):
        self.db = DB(os.path.join(self.librmo_config_dir, self.librmo_db_name))

    def execute(self) -> list:
        self._connect_librmo()
        self._get_album_groups()
        self._get_albumartists()
        self._query_album_releases()
        self._compare_releases()
        return self.missing_releases

    def __init__(self) -> None:
        self.mb = MBAPI()
