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


PROFILE_SCENARIOS = [
    (
        "High-Energy Pop",
        {
            "favorite_genre": "pop",
            "favorite_mood": "happy",
            "target_energy": 0.80,
            "likes_acoustic": False,
        },
    ),
    (
        "Chill Lofi",
        {
            "favorite_genre": "lofi",
            "favorite_mood": "chill",
            "target_energy": 0.35,
            "likes_acoustic": True,
        },
    ),
    (
        "Deep Intense Rock",
        {
            "favorite_genre": "rock",
            "favorite_mood": "intense",
            "target_energy": 0.92,
            "likes_acoustic": False,
        },
    ),
    (
        "Conflicted Sad High-Energy",
        {
            "favorite_genre": "pop",
            "favorite_mood": "sad",
            "target_energy": 0.90,
            "likes_acoustic": True,
        },
    ),
    (
        "Impossible Label Mismatch",
        {
            "favorite_genre": "edm",
            "favorite_mood": "sad",
            "target_energy": 0.15,
            "likes_acoustic": False,
        },
    ),
]


def print_recommendations(profile_name: str, user_prefs: dict, songs: list[dict]) -> None:
    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nMusic Recommender")
    print("=" * 72)
    print(f"Profile: {profile_name}")
    print(
        "Preferences:"
        f" genre={user_prefs['favorite_genre']},"
        f" mood={user_prefs['favorite_mood']},"
        f" target_energy={user_prefs['target_energy']:.2f},"
        f" likes_acoustic={user_prefs['likes_acoustic']}"
    )
    print("\nTop 5 recommendations:\n")

    for index, rec in enumerate(recommendations, start=1):
        song, score, explanation = rec
        reasons = [reason.strip().rstrip(".") for reason in explanation.split(";")]
        print(f"{index}. {song['title']} by {song['artist']}")
        print(f"   Final score: {score:.2f}")
        print("   Reasons:")
        for reason in reasons:
            print(f"   - {reason}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    for profile_name, user_prefs in PROFILE_SCENARIOS:
        print_recommendations(profile_name, user_prefs, songs)


if __name__ == "__main__":
    main()
