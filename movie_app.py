from iStorage import IStorage
from storage_json import StorageJson


# MovieApp class to manage movie commands and interactions
class MovieApp:
    def __init__(self, storage: IStorage):
        """
        Initializes the MovieApp with the provided storage.
        """
        self._storage = storage

    # List all movies in the database
    def _command_list_movies(self):
        """
        Lists all movies with their details such as rating and year.
        """
        movies = self._storage.list_movies()

        if movies:
            for title, movie_info in movies.items():
                rating = float(movie_info["rating"])
                year = movie_info["year"]
                print(f"{title}: {rating}, {year}")
        print()

    # Add a new movie to the database
    def _command_add_movie(self):
        """
        Adds a new movie using storage functionality.
        """
        self._storage.add_movie()

    # Delete a movie from the database
    def _command_delete_movie(self):
        """
        Deletes a movie from the database using the storage.
        """
        self._storage.delete_movie()

    # Update a movie's rating
    def _command_update_movie(self):
        """
        Updates the rating of an existing movie.
        """
        self._storage.update_movie()

    # Display statistics about the movies
    def _command_stats(self):
        """
        Displays statistics such as average and median ratings,
        and identifies the best and worst-rated movies.
        """
        movies = self._storage.list_movies()
        if not movies:
            return "No movies to display statistics."

        ratings = [movie_info["rating"] for movie_info in movies.values()]
        total_avg_rating = sum(ratings) / len(ratings)
        rounded_avg_rating = round(total_avg_rating, 1)
        print(f"Average rating: {rounded_avg_rating}")

        sorted_ratings = sorted(ratings)
        half_len = len(sorted_ratings) // 2
        if len(sorted_ratings) % 2 == 0:
            median_rating = (
                sorted_ratings[half_len - 1] + sorted_ratings[half_len]
            ) / 2
        else:
            median_rating = sorted_ratings[half_len]
            rounded_median_rating = round(median_rating, 1)
            print(f"Median rating: {rounded_median_rating}")

        best_rating = max(ratings)
        best_movies = [
            movie
            for movie, movie_info in movies.items()
            if movie_info["rating"] == best_rating
        ]
        print(f"The best movie(s) ({best_rating}): {', '.join(best_movies)}")

        worst_rating = min(ratings)
        worst_movies = [
            movie
            for movie, movie_info in movies.items()
            if movie_info["rating"] == worst_rating
        ]
        print(f"The worst movie(s) ({worst_rating}): {', '.join(worst_movies)}")

        print()

    # Randomly select and display a movie
    def _command_random_movie(self):
        """
        Selects and displays a random movie from the database.
        """
        import random

        movies = self._storage.list_movies()
        if not movies:
            print("No movies available.")
            return

        movie, movie_info = random.choice(list(movies.items()))
        print(f"Your movie for tonight: {movie}, it's rated: {movie_info['rating']}")

    # Search for a movie by name
    def _command_search_movie(self):
        """
        Searches for movies containing the provided substring in their name.
        """
        movie_name = input("Enter part of movie name: ")
        movies = self._storage.list_movies()
        found = False
        for name, movie_info in movies.items():
            if movie_name.lower() in name.lower():
                print(
                    f"{name}, Rating: {movie_info['rating']} Year: {movie_info['year']}"
                )
                found = True
        if not found:
            print("No movies found with that name.")

    # List movies sorted by their rating
    def _command_movies_sorted_by_rating(self):
        """
        Lists all movies sorted by their rating in descending order.
        """
        movies = self._storage.list_movies()
        sorted_movies = sorted(
            [(title, movie_info["rating"]) for title, movie_info in movies.items()],
            key=lambda x: x[1],
            reverse=True,
        )
        for movie, rating in sorted_movies:
            print(f"{movie}: {rating}")

    # Generate a website with a list of all movies
    def _command_generate_website(self):
        """
        Generates an HTML file listing all movies with their details.
        """
        movies = self._storage.list_movies()
        movie_grid = ""
        for title, info in movies.items():
            poster_url = info.get("Poster", "https://via.placeholder.com/150")
            movie_grid += f"""
            <li>
                <div class="movie">
                    <img class="movie-poster" src="{poster_url}" alt="Poster of {title}"/>
                    <div class="movie-title">{title}</div>
                    <div class="movie-year">{info.get('year', 'N/A')}</div>
                </div>
            </li>
            """

        try:
            with open("Static/index_template.html", "r") as file:
                template_data = file.read()
            html_content = template_data.replace("__TEMPLATE_TITLE__", "My Movie Page!")
            html_content = html_content.replace("__TEMPLATE_MOVIE_GRID__", movie_grid)
            with open("Static/index.html", "w") as file:
                file.write(html_content)
            print("Website was generated successfully.")
        except FileNotFoundError:
            print("Error: Template file not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    # Run the MovieApp to manage commands
    def run(self):
        """
        Runs the movie application and presents a menu for the user
        to interact with various functionalities.
        """
        while True:
            print("\nMenu:")
            print("0. Exit")
            print("1. List movies")
            print("2. Add movie")
            print("3. Delete movie")
            print("4. Update movie")
            print("5. Stats")
            print("6. Random movie")
            print("7. Search movie")
            print("8. Movies sorted by rating")
            print("9. Generate website\n")

            try:
                menu = int(input("Enter choice (0-9): "))
                print(f"User selected: {menu}")
                print()

                if menu == 0:
                    print("Exiting program. Goodbye!")
                    break
                elif menu == 1:
                    self._command_list_movies()
                elif menu == 2:
                    self._command_add_movie()
                elif menu == 3:
                    self._command_delete_movie()
                elif menu == 4:
                    self._command_update_movie()
                elif menu == 5:
                    self._command_stats()
                elif menu == 6:
                    self._command_random_movie()
                elif menu == 7:
                    self._command_search_movie()
                elif menu == 8:
                    self._command_movies_sorted_by_rating()
                elif menu == 9:
                    self._command_generate_website()
                else:
                    print("Invalid choice. Please enter a number between 0 and 9.")

                input("Press Enter to return to menu: ")

            except ValueError:
                print("Invalid input.")


# Main application to start MovieApp
storage = StorageJson("data.json")
movie_app = MovieApp(storage)
movie_app.run()
