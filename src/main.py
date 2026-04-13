"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

try:
    from src.recommender import load_songs, recommend_songs
except ModuleNotFoundError:
    from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Specific taste profile as a dictionary of target feature values.
    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.80,
        "likes_acoustic": False,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nMusic Recommender")
    print("=" * 72)
    print(
        "Profile:"
        f" genre={user_prefs['favorite_genre']},"
        f" mood={user_prefs['favorite_mood']},"
        f" target_energy={user_prefs['target_energy']:.2f},"
        f" likes_acoustic={user_prefs['likes_acoustic']}"
    )
    print("\nTop recommendations:\n")

    for index, rec in enumerate(recommendations, start=1):
        song, score, explanation = rec
        reasons = [reason.strip().rstrip(".") for reason in explanation.split(";")]
        print(f"{index}. {song['title']} by {song['artist']}")
        print(f"   Final score: {score:.2f}")
        print("   Reasons:")
        for reason in reasons:
            print(f"   - {reason}")
        print()


if __name__ == "__main__":
    main()
