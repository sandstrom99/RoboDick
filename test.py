import imdb


try:
    ia = imdb.Cinemagoer()
    search = "matrix"
    movies = ia.search_movie(search)
    print(movies)
except imdb.IMDbError as e:
    print(e)
