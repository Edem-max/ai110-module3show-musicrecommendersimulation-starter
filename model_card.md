# 🎧 Model Card: Music Recommender Simulation

## Model Name

**VibeScout 1.0**

## Goal / Task

This model suggests songs from a small music catalog.
It tries to find songs that match a user's genre, mood, energy, and acoustic preference.
It returns the top 5 songs with short explanations.

## Data Used

The dataset has 18 songs in `data/songs.csv`.
Each song has a title, artist, genre, mood, energy, tempo, valence, danceability, and acousticness.
The model only scores genre, mood, energy, and acousticness.
The catalog is small, so many music styles are missing.
I did not add or remove songs.

## Algorithm Summary

The model gives each song a score.
It adds 2 points for a genre match.
It adds 1 point for a mood match.
It adds more points when the song's energy is close to the user's target energy.
It adds a small bonus when the song's acousticness matches the user's acoustic preference.
Then it sorts the songs by score and returns the top 5.

## Observed Behavior / Biases

The model works best when the user asks for labels that exist in the dataset.
Genre has the biggest weight, so it can dominate the results.
If the user's genre or mood is missing, the model still recommends songs based on energy and acousticness.
That can lead to strange results.
The model also ignores tempo, valence, and danceability even though those features are in the data.

## Evaluation Process

I tested five profiles.
The first three were normal profiles: `High-Energy Pop`, `Chill Lofi`, and `Deep Intense Rock`.
The last two were edge cases: `Conflicted Sad High-Energy` and `Impossible Label Mismatch`.
I looked at the top 5 recommendations for each profile in the terminal.
I compared whether the results felt reasonable based on the profile.
The edge cases showed where the scoring logic can be tricked or stretched.

## Intended Use and Non-Intended Use

This system is meant for classroom learning.
It is good for showing how a simple recommender turns user preferences into scores.
It is not meant for real music streaming apps.
It should not be used for high-stakes decisions or for judging real user taste in a complete way.

## Ideas for Improvement

- Add user preferences for tempo, valence, and danceability.
- Reduce the genre weight so one feature does not control the ranking too much.
- Add a diversity rule so the top 5 are not too similar.

## Personal Reflection

My biggest learning moment was seeing how a few simple scoring rules could still create recommendations that felt believable. Genre match, mood match, and energy similarity were enough to make many of the results feel personal, even without machine learning. At the same time, the edge-case profiles showed me that a system can look correct in the output while still missing what a user really meant.

AI tools helped me move faster when I was brainstorming test profiles, organizing my explanations, and thinking about how to describe the system clearly. I still needed to double-check those ideas against the actual code and terminal output. Sometimes an AI suggestion sounded reasonable, but the recommender behaved differently once I ran it, so I had to verify everything with real results.

What surprised me most was that simple algorithms can still feel smart because they reward familiar features in a way that seems personalized. If I extended this project, I would add more user preferences like tempo, valence, and danceability, test more unusual user profiles, and improve the ranking so the top results are more diverse and less dependent on exact labels.
