import csv
from iStorage import IStorage


class StorageCsv(IStorage):
    def __init__(self, file_path):
        self.file_path = file_path
        self.movies = (
            self.load_movies()
        )  # load movies from the CSV file on initialization

    def load_movies(self):
        """Load movies from the CSV file and return as a dictionary."""
        movies = {}
        try:
            with open(self.file_path, mode="r", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    title = row["title"]
                    movies[title] = {
                        "rating": float(row["rating"]),
                        "year": int(row["year"]),
                        "Poster": row.get("Poster", ""),
                    }
        except FileNotFoundError:
            # if the file does not exist, return an empty dict
            pass
        return movies

    def save_movies(self):
        """Save the movies dictionary to the CSV file."""
        with open(self.file_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["title", "rating", "year", "Poster"])  # write header
            for title, movie_info in self.movies.items():
                writer.writerow(
                    [
                        title,
                        movie_info["rating"],
                        movie_info["year"],
                        movie_info.get("Poster", ""),
                    ]
                )

    def list_movies(self):
        """Return the movies dictionary."""
        return self.movies

    def add_movie(self, title, year, rating, poster):
        """Add a movie to the storage."""
        self.movies[title] = {"rating": rating, "year": year, "Poster": poster}
        self.save_movies()  # save changes to the CSV file

    def delete_movie(self, title):
        """Delete a movie from the storage."""
        if title in self.movies:
            del self.movies[title]
            self.save_movies()
        else:
            print(f"Movie '{title}' not found in the list.")

    def update_movie(self, title, rating):
        """Update the rating of an existing movie."""
        if title in self.movies:
            self.movies[title]["rating"] = rating
            self.save_movies()  # Save changes
        else:
            print(f"Movie '{title}' not found in the list.")
