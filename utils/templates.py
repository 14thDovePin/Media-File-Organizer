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
        """Generate a metadata dictionary.

        Returns
        -------
        metadata : dict
            Dictionary Keys:
            - **title** : str
            - **type** : str
                Set to either "movie" or "series".
            - **year** : str
            - **season** : str
            - **episode** : str
            - **imdb_id** : str
        """

        return {
            "title" : "",
            "type" : "",
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
