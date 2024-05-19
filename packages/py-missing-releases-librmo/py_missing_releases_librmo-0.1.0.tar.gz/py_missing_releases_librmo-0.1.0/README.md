# Py-Missing-Releases-LibRMO

With a media library set up by LibRMO you can use this application to query its database and return a list of missing releases from the artists you have

# Usage

Will take some time to acquire the responses from MusicBrainz (1s per existing release and then 1s per artist), but results are cached in MusicBrainzAPI.

```python
import pprint

from py_missing_releases_librmo import MissingReleases

mr = MissingReleases()
result = mr.execute()
pprint.pprint(result[::10])
pprint.pprint(f"Missing albums: {len(result)}")
```

```
[Release(name='Down to Earth',
         artist=AlbumArtist(name='Ozzy Osbourne',
                            mb_id='8aa5b65a-5b3c-4029-92bf-47a544356934'),
         mb_id='c76e9935-1cef-3339-930f-cf1914fd1037',
         url=''),
 Release(name='Cavalry in Thousands',
         artist=AlbumArtist(name='Tengger Cavalry',
                            mb_id='71c53622-5e7d-44da-90d3-30ea2c89ad0e'),
         mb_id='f0af6659-cef4-4397-aa28-5773d04c96fb',
         url=''),
...
...
'Missing albums: 519'
```
