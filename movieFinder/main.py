from movieFinder.download_movies import store_movies
from movieFinder.upload_github import upload_to_github


def main():
    store_movies()
    upload_to_github()

if __name__ == "__main__":
    main()
