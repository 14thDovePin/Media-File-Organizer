class GenerateTemplate():
    """A class for generating templates."""

    def media_data(self) -> dict:
        """Generate a video file information dictionary.

        Returns
        -------
        media_data : dict
            Dictionary Keys:
            - **title_sequence** : list
            - **metadata** : dict
            - **file_information** : dict
        """

        return {
            "title_sequence" : [],
            "metadata" : {},
            "file_information" : {}
        }


    def metadata(self) -> dict:
        """Create and return a media information dictionary.

        Returns
        -------
        dict
            title : str
            media_type : str
            year : int
            season : int
            episode : int
            imdb_id : str
        """

        return {
            "title" : "",
            "media_type" : "",
            "year" : "",
            "season" : "",
            "episode" : "",
            "imdb_id" : ""
        }

    def file_info(self) -> dict:
        """Generate a file information dictionary.

        Returns
        -------
        file_info : dict
            Dictionary Keys:
            - **filename** : str
            - **new_filename** : str
            - **extension** : str
            - **path** : str
        """

        return {
            "filename" : "",
            "new_filename" : "",
            "extension" : "",
            "path" : "",
        }

    def media_info(self, is_show: False) -> dict:
        """Create and return a dictionary to house related information of media.

        Parameters
        ----------
        is_show : bool, default=False
            If specified as true, season, and episode key-value
            pairs are added to the dict before returning.

        Returns
        -------
        dict
        """
        media_dict = {
            "title" : "",
            "media_type" : "Movie",
            "year" : int(),
            "imdb_id" : ""
        }

        if is_show:
            media_dict["media_type"] = "Show"
            media_dict["Season"] = int()
            media_dict["Episode"] = int()

        return media_dict