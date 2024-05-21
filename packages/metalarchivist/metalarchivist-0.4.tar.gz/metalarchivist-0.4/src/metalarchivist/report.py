import string
from typing import Callable
from datetime import datetime
from dataclasses import asdict

from .export import Band, Album, Label

Datum = str | int | float | None
Series = list[Datum]
Record = dict[str, Datum]
Dataset = list[Record]


def series(from_list: list[dict], column: str) -> Series:
    return [[v for k, v in d.items() if k == column][0] for d in from_list]


def select(from_list: list[dict], column: str) -> Dataset:
    return list(map(lambda n: {column: n[column]}, from_list))


def expand(from_list: list, column: str) -> Dataset:
    column_sample: Record = next(filter(lambda n: n[column], from_list))[column]
    null_dict: Record = {str(k): None for k in column_sample.keys()}
    return list(map(lambda n: dict(**n[column]) if n[column] else null_dict, from_list))


def where(from_list: list, column: str, key: Callable[[Datum], bool]) -> Dataset:
    return [n for n in from_list if key(n[column])]


def drop(from_list: list[dict], *columns: str) -> Dataset:
    return [{k: v for k, v in d.items() if k not in columns} for d in from_list]


def rename(from_list: list, column_map: dict) -> Dataset:
    return [{column_map.get(k, k): v for k, v in d.items()} for d in from_list]


def join(first_list: Dataset, second_list: Dataset, on_column: str) -> Dataset:
    return [dict(**left, **{k: v for k, v in right.items() if k not in left}) 
            for left in first_list for right in second_list 
            if left[on_column] == right[on_column]]


def get_bands(profile_urls: list[str], wait=3.) -> Dataset:
    band_profile = Band.get_profiles(profile_urls, wait=wait)
    band_profile = list(map(lambda n: n.to_dict(), band_profile))
    
    band_desc = expand(select(band_profile, 'description'), 'description')
    band_desc = drop(band_desc, 'genre', 'themes', 'lyrical_themes')

    band_ids = series(band_profile, 'metallum_id')
    band_ids = [int(band_id) for band_id in band_ids if band_id is not None]
    band_links = Band.get_external_links(band_ids, wait=wait)
    band_links = list(map(asdict, band_links))

    genres = expand(select(band_profile, 'genres'), 'genres')
    themes = expand(select(band_profile, 'themes'), 'themes')

    band_profile = drop(band_profile, 'genres', 'themes',  'description')
    band_profile = join(band_profile, band_links, 'metallum_id')

    band_zip = zip(band_profile, band_desc, genres, themes)

    return [dict(**bp, **bd, **g, **t) for bp, bd, g, t in band_zip]


def get_album_profiles(profile_urls: list[str]) -> Dataset:
    album_profile = Album.get_profiles(profile_urls)
    album_profile = list(map(lambda n: n.to_dict(), album_profile))
    return album_profile


def get_albums(range_start: datetime | None = None, range_stop: datetime | None = None, 
               wait=3., retries=3, timeout=3.) -> Dataset:
    if range_start:
        release_page = Album.get_range(range_start, range_stop, wait=wait, retries=retries, 
                                       timeout_cxn=timeout, timeout_read=timeout * 3)
    else:
        release_page = Album.get_upcoming(wait=wait, retries=retries, timeout_cxn=timeout, 
                                          timeout_read=timeout * 3)

    release = list(map(asdict, release_page.data))

    band_key = select(expand(select(release, 'band'), 'band'), 'band_key')
    
    # hoist out the link attributes from each band
    profile_urls = select(expand(select(release, 'band'), 'band'), 'link')
    profile_urls = series(profile_urls, 'link')
    profile_urls = [str(p) for p in profile_urls]

    band = get_bands(profile_urls, wait=wait)

    album = expand(select(release, 'album'), 'album')
    album = rename(album, dict(name='album', link='album_url'))

    album_url = series(album, 'album_url')
    album_url = [str(u) for u in album_url]
    album_profiles = get_album_profiles(album_url)
    album = join(album, album_profiles, 'album_key')
    album = drop(album, 'band')

    label_link = select(album, 'label')
    label_link = expand(label_link, 'label')
    label_key = select(label_link, 'label_key')

    label_url = where(label_link, 'link', lambda n: n is not None)
    label_url = series(label_url, 'link')
    label_url = [str(u) for u in label_url]
    label = get_label_profiles(label_url)
    label = rename(label, dict(profile='label_profile',
                               roster='label_roster',
                               releases='label_releases'))
    
    band = rename(band, dict(url='band_url', name='band'))
    release = drop(release, 'genres', 'band', 'album', 'release_type')
    
    album = drop(album, 'label')
    album = zip(album, band_key, label_key, release)
    album = [dict(**a, **b, **lb, **r) for a, b, lb, r in album]
    album = join(album, band, 'band_key')
    album = join(album, label, 'label_key')

    return album


def get_labels() -> Dataset:
    label = Label.get_labels_by_letters(*string.ascii_lowercase, page_size=1000)
    label = map(lambda n: n.label.url, label.data)
    label = map(Label.get_full_profile, label)
    label = map(asdict, label)
    label = list(label)

    return label


def get_label_profiles(profile_urls: list[str]) -> Dataset:
    label_container = Label.get_full_profiles(profile_urls)
    label_container = list(map(lambda n: n.to_dict(), label_container))
    
    label_key = select(label_container, 'label_key')
    label_links = select(label_container, 'links')
    label_releases = select(label_container, 'releases')
    label_roster = select(label_container, 'roster')
    label_profile = select(label_container, 'profile')
    
    label_roster = rename(label_roster, dict(current='roster_current', past='roster_past'))
    label_links = select(label_links, 'links')

    label = zip(label_key, label_profile, label_releases, label_roster, label_links)
    label = [dict(**key, **profile, **albums, **roster, **links) 
             for key, profile, albums, roster, links in label]

    return label



def get_genres():
    ...
