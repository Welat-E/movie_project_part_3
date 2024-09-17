from abc import ABC, abstractmethod


class IStorage(ABC):
    @abstractmethod
    def list_movies(self):
        """Shows all movies from storage."""
        pass

    @abstractmethod
    def add_movie(self, title, year, rating, poster):
        """Adds movie to the storage from api."""
        pass

    @abstractmethod
    def delete_movie(self, title):
        """Deletes movies from storage."""
        pass

    @abstractmethod
    def update_movie(self, title, rating):
        """Updates the rating of a movie."""
        pass
