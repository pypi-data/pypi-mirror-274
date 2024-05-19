Simple minded facilities for media information.
This contains mostly lexical functions
for extracting information from strings
or constructing media filenames from metadata.

*Latest release 20240519*:
Initial PyPI release, particularly for SeriesEpisodeInfo which I use in cs.app.playon.

The default filename parsing rules are based on my personal convention,
which is to name media files as:

  series_name--episode_info--title--source--etc-etc.ext

where the components are:
* `series_name`:
  the programme series name downcased and with whitespace replaced by dashes;
  in the case of standalone items like movies this is often the studio.
* `episode_info`: a structures field with episode information:
  `s`_n_ is a series/season,
  `e`_n_` is an episode number within the season,
  `x`_n_` is a "extra" - addition material supplied with the season,
  etc.
* `title`: the episode title downcased and with whitespace replaced by dashes
* `source`: the source of the media
* `ext`: filename extension such as `mp4`.

As you may imagine,
as a rule I dislike mixed case filenames
and filenames with embedded whitespace.
I also like a media filename to contain enough information
to identify the file contents in a compact and human readable form.

## Class `EpisodeDatumDefn(EpisodeDatumDefn)`

An `EpisodeInfo` marker definition.

*Method `EpisodeDatumDefn.parse(self, s, offset=0)`*:
Parse an episode datum from a string, return the value and new offset.
Raise `ValueError` if the string doesn't match this definition.

Parameters:
* `s`: the string
* `offset`: parse offset, default 0

## Class `EpisodeInfo(types.SimpleNamespace)`

Trite class for episodic information, used to store, match
or transcribe series/season, episode, etc values.

*Method `EpisodeInfo.__getitem__(self, name)`*:
We can look up values by name.

*Method `EpisodeInfo.as_dict(self)`*:
Return the episode info as a `dict`.

*Method `EpisodeInfo.as_tags(self, prefix=None)`*:
Generator yielding the episode info as `Tag`s.

*Method `EpisodeInfo.from_filename_part(s, offset=0)`*:
Factory to return an `EpisodeInfo` from a filename episode field.

Parameters:
* `s`: the string containing the episode information
* `offset`: the start of the episode information, default 0

The episode information must extend to the end of the string
because the factory returns just the information. See the
`parse_filename_part` class method for the core parse.

*Method `EpisodeInfo.get(self, name, default=None)`*:
Look up value by name with default.

*Method `EpisodeInfo.parse_filename_part(s, offset=0)`*:
Parse episode information from a string,
returning the matched fields and the new offset.

Parameters:
`s`: the string containing the episode information.
`offset`: the starting offset of the information, default 0.

*Property `EpisodeInfo.season`*:
.season property, synonym for .series

## Function `main(argv=None)`

Main command line running some test code.

## Function `parse_name(name, sep='--')`

Parse the descriptive part of a filename
(the portion remaining after stripping the file extension)
and yield `(part,fields)` for each part as delineated by `sep`.

## Function `part_to_title(part)`

Convert a filename part into a title string.

Example:

    >>> part_to_title('episode-name')
    'Episode Name'

## Function `pathname_info(pathname)`

Parse information from the basename of a file pathname.
Return a mapping of field => values in the order parsed.

## Function `scrub_title(title: str, *, season=None, episode=None) -> str`

Strip redundant text from the start of an episode title.

I frequently get "title" strings with leading season/episode information.
This function cleans up these strings to return the unadorned title.

## Class `SeriesEpisodeInfo(cs.deco.Promotable)`

Episode information from a TV series episode.

*Method `SeriesEpisodeInfo.as_dict(self)`*:
Return the non-`None` values as a `dict`.

*Method `SeriesEpisodeInfo.from_str(episode_title: str, series=None)`*:
Infer a `SeriesEpisodeInfo` from an episode title.

This recognises the common `'sSSeEE - Episode Title'` format
and variants like `Series Name - sSSeEE - Episode Title'`
or `'sSSeEE - Episode Title - Part: One'`.

## Function `title_to_part(title)`

Convert a title string into a filename part.
This is lossy; the `part_to_title` function cannot completely reverse this.

Example:

    >>> title_to_part('Episode Name')
    'episode-name'

# Release Log



*Release 20240519*:
Initial PyPI release, particularly for SeriesEpisodeInfo which I use in cs.app.playon.
