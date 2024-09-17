from storage_csv import StorageCsv
from movie_app import MovieApp

# Main function to run the Movie App

def main():
    """
    Main function to create instances of StorageCsv and MovieApp, 
    and to run the movie application.
    """
    print("Starting MovieApp...") 
    
    # Create an instance of StorageCsv
    storage = StorageCsv('movies.csv')

    # Create an instance of MovieApp with the StorageCsv object
    movie_app = MovieApp(storage)

    # Run the application
    movie_app.run()


if __name__ == "__main__":
    main()

