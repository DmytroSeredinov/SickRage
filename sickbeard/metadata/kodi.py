# coding=utf-8

# Author: Nic Wolfe <nic@wolfeden.ca>
# URL: https://sickrage.github.io
#
# This file is part of SickRage.
#
# SickRage is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SickRage is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SickRage. If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

import os

from sickbeard.metadata import generic, kodi_12plus
from sickrage.helper.common import replace_extension
from sickrage.helper.encoding import ek


class KODIMetadata(kodi_12plus.KODI_12PlusMetadata):
    """
    Metadata generation class for KODI (legacy).

    The following file structure is used:

    show_root/tvshow.nfo              (show metadata)
    show_root/fanart.jpg              (fanart)
    show_root/folder.jpg              (poster)
    show_root/folder.jpg              (banner)
    show_root/Season ##/filename.ext  (*)
    show_root/Season ##/filename.nfo  (episode metadata)
    show_root/Season ##/filename.tbn  (episode thumb)
    show_root/season##.tbn            (season posters)
    show_root/season-all.tbn          (season all poster)
    """

    def __init__(self,
                 show_metadata=False,
                 episode_metadata=False,
                 fanart=False,
                 poster=False,
                 banner=False,
                 episode_thumbnails=False,
                 season_posters=False,
                 season_banners=False,
                 season_all_poster=False,
                 season_all_banner=False):

        generic.GenericMetadata.__init__(self,
                                         show_metadata,
                                         episode_metadata,
                                         fanart,
                                         poster,
                                         banner,
                                         episode_thumbnails,
                                         season_posters,
                                         season_banners,
                                         season_all_poster,
                                         season_all_banner)

        self.name = 'KODI'

        self.poster_name = self.banner_name = "folder.jpg"
        self.season_all_poster_name = "season-all.tbn"

        # web-ui metadata template
        self.eg_show_metadata = "tvshow.nfo"
        self.eg_episode_metadata = "Season##\\<i>filename</i>.nfo"
        self.eg_fanart = "fanart.jpg"
        self.eg_poster = "folder.jpg"
        self.eg_banner = "folder.jpg"
        self.eg_episode_thumbnails = "Season##\\<i>filename</i>.tbn"
        self.eg_season_posters = "season##.tbn"
        self.eg_season_banners = "<i>not supported</i>"
        self.eg_season_all_poster = "season-all.tbn"
        self.eg_season_all_banner = "<i>not supported</i>"

    # Override with empty methods for unsupported features
    def create_season_banners(self, ep_obj):
        pass

    def create_season_all_banner(self, show_obj):
        pass

    @staticmethod
    def get_episode_thumb_path(ep_obj):
        """
        Returns the path where the episode thumbnail should be stored. Defaults to
        the same path as the episode file but with a .tbn extension.

        ep_obj: a TVEpisode instance for which to create the thumbnail
        """
        if ek(os.path.isfile, ep_obj.location):
            tbn_filename = replace_extension(ep_obj.location, 'tbn')
        else:
            return None

        return tbn_filename

    @staticmethod
    def get_season_poster_path(show_obj, season):
        """
        Returns the full path to the file for a given season poster.

        show_obj: a TVShow instance for which to generate the path
        season: a season number to be used for the path. Note that season 0
                means specials.
        """

        # Our specials thumbnail is, well, special
        if season == 0:
            season_poster_filename = 'season-specials'
        else:
            season_poster_filename = 'season' + str(season).zfill(2)

        return ek(os.path.join, show_obj.location, season_poster_filename + '.tbn')


# present a standard "interface" from the module
metadata_class = KODIMetadata
