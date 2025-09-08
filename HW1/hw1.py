# CS4412 : Data Mining
# Kennesaw State University
#Author: Youssef El-Shaer
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

# produce a map from movie_id to the movie's title
movie_titles = dict()
for movie in movie_data:
    # each line in the dataset has an ID, title, and list of genre's
    movie_id,title,genres = movie
    movie_titles[movie_id] = title

# produce a map from movie_id to the movie's genres
movie_genres = dict()
for movie in movie_data:
    movie_id,title,genres = movie
    # the list of genre is seperated by a | character
    genres = genres.split('|')
    movie_genres[movie_id] = genres

# next, we compute the average rating for each movie
# first, initialize counts and sums
counts = {}  # number of ratings
sums = {}    # sum of all ratings
user_ratings = set() # set

for rating in rating_data:
    # each line in the dataset has a user-ID, movie-ID, score, and timestamp
    user_id, movie_id, score, timestamp = rating
    score = float(score)
    if movie_id == "260" and score == 5.0:
        user_ratings.add(user_id)

# count and sum the ratings for each movie
for rating in rating_data:
    user_id,movie_id,score,timestamp = rating
    # in the dataset, all fields are strings, so convert the score to
    # a floating-point number first when we compute the average rating
    score = float(score)
    if user_id in user_ratings:
        counts[movie_id] = counts.get(movie_id,0) + 1
        sums[movie_id] = sums.get(movie_id,0) + score

# compute the averages from the counts and sums
stats = {}
min_ratings = 10
for movie_id in counts:
    if counts[movie_id] < min_ratings or movie_id == "260": continue
    average = sums[movie_id]/counts[movie_id]
    # each stat entry has the movie id, the average rating, and #-of-ratings
    stats[movie_id] = (movie_id,average,counts[movie_id])

# sort the list of ratings
key_function = lambda x: x[1] # given x, return x[1]
ranking = list(stats.values())
ranking.sort(key=key_function, reverse=True)

#print the movie with the highest average rating
print("============================================")
print("== Movie with Highest Average Rating")
print("============================================")
if ranking:
    # each stat entry has the movie id, the average rating, and #-of-ratings
    top_movie_id,top_average,top_count = ranking[0]
    top_movie_title = movie_titles[top_movie_id]
    print('%40s: %.2f (%d ratings)' % (top_movie_title[:40],top_average,top_count))