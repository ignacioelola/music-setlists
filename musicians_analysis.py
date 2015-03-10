__author__ = 'ignacioelola'

import csv
import numpy as np

'''
Cleaning:
- Check that musician = musician from show
- One musician in multiple genres think about structure (musician -> genre or genre -> musician)
Analysis:
- structure genre - musician - year - show - songs
- # different songs per musician - rank them
- avg # of different songs per genre
- Hard working / best memory artists VS lazy artists
- Model to predict songs of Lazy artists
- Which musical genre has more heterogenity in lazyness
- Clustering musical genres, discovering groups of artists
- sSearch for outliers!
'''


def clean_musicians(infile):

    cleaned_data = {}
    with open(infile, "r") as f:
        reader = csv.reader(f)
        for row_count, row in enumerate(reader):
            if row_count > 0:
                genre = row[0]
                musician = row[1]
                if "list of" not in musician.lower() and "lists of" not in musician.lower():
                    if genre not in cleaned_data:
                        cleaned_data[genre] = []
                    cleaned_data[genre].append(musician)

    return cleaned_data


def clean_live_songs(infile):

    cleaned_data = {}
    with open(infile, "r") as f:
        reader = csv.reader(f)
        for row_count, row in enumerate(reader):
            if row_count > 0:
                musician = row[0]
                show = row[1]
                year = row[2]
                song = row[3]
                musician_from_show = show[:show.find(" at ")]
                if musician_from_show.lower().replace("the ", "") == musician.lower().replace("the ", ""):
                    if musician not in cleaned_data:
                        cleaned_data[musician] = {}
                    if year not in cleaned_data[musician]:
                        cleaned_data[musician][year] = {}
                    if show not in cleaned_data[musician][year]:
                        cleaned_data[musician][year][show] = []
                    cleaned_data[musician][year][show].append(song)

    return cleaned_data


def merge_genres_live_songs(genres_musicians, musicians_live_songs):

    genres_live_songs = {}
    for genre in genres_musicians:
        for musician in genres_musicians[genre]:
            if musician in musicians_live_songs:
                if genre not in genres_live_songs:
                    genres_live_songs[genre] = {}
                if musician not in genres_live_songs[genre]:
                    genres_live_songs[genre][musician] = []
                for year in musicians_live_songs[musician]:
                    for show in musicians_live_songs[musician][year]:
                        for song in musicians_live_songs[musician][year][show]:
                            genres_live_songs[genre][musician].append(song)

    return genres_live_songs


def calculate_diversity(genres_live_songs, musicians_live_songs):

    genres_musicians_diversity = {}
    for genre in genres_live_songs:
        if genre not in genres_musicians_diversity:
            genres_musicians_diversity[genre] = {}
        for musician in genres_live_songs[genre]:
            repetition = float(len(genres_live_songs[genre][musician]))/float(len(set(genres_live_songs[genre][musician])))
            genres_musicians_diversity[genre][musician] = repetition

    return genres_musicians_diversity


def main():

    musicians_genres_file = "data/musicians.csv"
    musicians_live_songs_file = "data/live_songs.csv"

    genres_musicians = clean_musicians(musicians_genres_file)
    musicians_live_songs = clean_live_songs(musicians_live_songs_file)

    genres_live_songs = merge_genres_live_songs(genres_musicians, musicians_live_songs)
    print "%s genres" % len(genres_live_songs)
    num_musicians = 0
    for genre in genres_live_songs:
        num_musicians += len(genres_live_songs[genre])
    print "%s musicians" % num_musicians
    num_songs = 0
    for genre in genres_live_songs:
        for musician in genres_live_songs[genre]:
            num_songs += len(genres_live_songs[genre][musician])
    print "%s songs" % num_songs

    genres_musicians_diversity = calculate_diversity(genres_live_songs, musicians_live_songs)
    for genre in genres_musicians_diversity:
        repetition = []
        for musician in genres_musicians_diversity[genre]:
            repetition.append(genres_musicians_diversity[genre][musician])
            # print "%s\t%s\t%s" % (genre, musician, repetition)
        print "%s\t%s" % (genre, np.mean(repetition))



if __name__ == '__main__':

    main()
