# CS4412 : Data Mining
# Kennesaw State University
# Author: Youssef El-Shaer
# Homework 1

# module for reading csv files
import csv

def read_csv_file(filename):
    """this function reads a .CSV file, and returns the dataset as a list"""
    with open(filename,'r',encoding='utf-8') as f:
        reader = csv.reader(f,delimiter=',', quotechar='"')
        dataset = [ line for line in reader ]
    return dataset

# read the datasets from file
movie_data = read_csv_file("data/movies.csv")
rating_data = read_csv_file("data/ratings.csv")

# skip the headers in the datasets
movie_data = movie_data[1:]
rating_data = rating_data[1:]

# produce a map from movie_id to the movie'score title
movie_titles = dict()
for movie in movie_data:
    # each line in the dataset has an ID, title, and list of genre'score
    movie_id,title,genres = movie
    movie_titles[movie_id] = title

# produce a map from movie_id to the movie'score genres
movie_genres = dict()
for movie in movie_data:
    movie_id,title,genres = movie
    # the list of genre is seperated by a | character
    genres = genres.split('|')
    movie_genres[movie_id] = genres

# Helper: Compute average ratings from rating rows, with optional filters:
#   - include_genre: only movies with this genre
#   - exclude_movie_ids: skip these movies
#   - min_ratings: minimum ratings required
def compute_stats_from_ratings(filtered_rating_rows, min_ratings=1, include_genre=None, exclude_movie_ids=None):
    counts = {}
    sums = {}
    for user_id, movie_id, score, timestamp in filtered_rating_rows:
        if exclude_movie_ids and movie_id in exclude_movie_ids:
            continue
        score = float(score)
        if include_genre is not None:
            if movie_id not in movie_genres or include_genre not in movie_genres[movie_id]:
                continue
        counts[movie_id] = counts.get(movie_id, 0) + 1
        sums[movie_id] = sums.get(movie_id, 0.0) + score

    stats = {}
    for movie_id in counts:
        if counts[movie_id] < min_ratings:
            continue
        stats[movie_id] = (movie_id, sums[movie_id] / counts[movie_id], counts[movie_id])
    return stats

# Build set of users who rated movie '260' a 5.0, then compute stats from their ratings (excluding '260')
FAVORITE_MOVIE_ID = '260'
FAVORITE_SCORE = 5.0

# create a set of users who rated movie 260 as 5.0
user_ratings = set()
for user_id, movie_id, score, timestamp in rating_data:
    if movie_id == FAVORITE_MOVIE_ID and float(score) == FAVORITE_SCORE:
        user_ratings.add(user_id)

# filter the dataset so only ratings from these users are included
filtered_rows = [row for row in rating_data if row[0] in user_ratings]

# compute stats with min_ratings=10 and exclude movie 260
stats = compute_stats_from_ratings(
    filtered_rows,
    min_ratings=10,
    include_genre=None,
    exclude_movie_ids={FAVORITE_MOVIE_ID}
)

# sort the list of ratings
ranking = list(stats.values())
ranking.sort(key=lambda x: x[1], reverse=True)

# print the movie with the highest average rating
print("============================================")
print("== Top movie among users who gave '260' a 5.0 (min 10 ratings, excluding 260)")
print("============================================")
if ranking:
    top_movie_id, top_average, top_count = ranking[0]
    top_movie_title = movie_titles.get(top_movie_id, f"(unknown #{top_movie_id})")
    print(f"{top_movie_title}: {top_average:.2f} ({top_count} ratings)")
else:
    print("No qualifying movies found.")

# --- Helpers for genre stats: highest/lowest average with ≥100 ratings ---
def top_in_genre(movie_genre_name, min_ratings=100):
    genre_stats = compute_stats_from_ratings(
        rating_data,
        min_ratings=min_ratings,
        include_genre=movie_genre_name,
        exclude_movie_ids=None
    )
    if not genre_stats:
        return None
    best = max(genre_stats.values(), key=lambda x: x[1])
    movie_id, avg, cnt = best
    return (movie_id, movie_titles.get(movie_id, f"(unknown #{movie_id})"), avg, cnt)

def bottom_in_genre(movie_genre_name, min_ratings=100):
    genre_stats = compute_stats_from_ratings(
        rating_data,
        min_ratings=min_ratings,
        include_genre=movie_genre_name,
        exclude_movie_ids=None
    )
    if not genre_stats:
        return None
    worst = min(genre_stats.values(), key=lambda x: x[1])
    movie_id, avg, cnt = worst
    return (movie_id, movie_titles.get(movie_id, f"(unknown #{movie_id})"), avg, cnt)

# answers to your two questions
mystery_top = top_in_genre("Mystery", min_ratings=100)
action_bottom = bottom_in_genre("Action", min_ratings=100)

print("\n== Q1: Highest average in Mystery (>=100 ratings)")
if mystery_top:
    movie_id, title, avg, cnt = mystery_top
    print(f"{title}: {avg:.2f} ({cnt} ratings)")
else:
    print("No qualifying Mystery titles found.")

print("\n== Q2: Lowest average in Action (>=100 ratings)")
if action_bottom:
    movie_id, title, avg, cnt = action_bottom
    print(f"{title}: {avg:.2f} ({cnt} ratings)")
else:
    print("No qualifying Action titles found.")