from iStorage import IStorage
import json
import requests
from config.config_files import APIkeys


class StorageJson(IStorage):
    def __init__(self, file_path):
        self.file_path = file_path
        #load the JSON file and save the data as a dict
        self.movies = self.load()


    def load(self):
        """Loads JSON FILE"""
        try:
            with open(self.file_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}  #return an empty dictionary if the file does not exist


    def save(self):
        """Saves the movies dictionary to the JSON FILE"""
        with open(self.file_path, "w") as f:
            json.dump(self.movies, f, indent=4)


    def list_movies(self):
        """Gives all movies from dict"""
        return self.movies


    def add_movie(self):
        """Adds movie to storage"""
        try:
            key = input("Enter new movie name: ")
            url = f"http://www.omdbapi.com/?apikey={APIkeys.APIkey}&t={key}"
            response = requests.get(url)

            #print(response.json()) 

            if response.status_code == 200:
                response2 = response.json()
                if "Title" in response2:
                    print(f"{response2['Title']} is added now to your movie list.")

                    values = {
                        "rating": float(response2["imdbRating"]),
                        "year": int(response2["Year"]),
                        "Poster": response2["Poster"],
                    }

                    self.movies[key] = (
                        values  #saving the new movie in the class attribute
                    )
                    self.save()  #save changes to the file
                else:
                    print("Movie not found.")
            else:
                print(f"Error: {response.status_code}")
        except Exception as e:
            print(e)


    def delete_movie(self):
        """Deletes movies from the storage"""
        del_movie = input("Enter a movie to delete: ")
        if del_movie in self.movies:
            del self.movies[del_movie]
            print(f"{del_movie} got deleted.")
            self.save()  #save changes to the file
        else:
            print("This movie is not in your list.")
        return self.movies


    def update_movie(self):
        """Update the rating of an existing movie."""
        edit_movie = input("Enter movie name: ")
        if edit_movie in self.movies:
            movie_info = self.movies[edit_movie]
            new_rating = float(input("Enter new rating: "))
            movie_info["rating"] = new_rating
            self.movies[edit_movie] = movie_info
            print(f"Movie {edit_movie} successfully updated")
            self.save()  # Save changes to the file
        else:
            print("The movie doesn't exist")
        return self.movies


# Create an instance of the StorageJson class
storage = StorageJson("data.json")
