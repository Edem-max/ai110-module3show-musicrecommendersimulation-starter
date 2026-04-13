from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        ranked_songs = sorted(
            self.songs,
            key=lambda song: score_song(song, user),
            reverse=True,
        )
        return ranked_songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        return build_explanation(song, user)


def score_song(song: Song, user: UserProfile) -> float:
    """Return only the numeric recommendation score for one song."""
    score, _ = score_song_with_reasons(song, user)
    return score


def score_song_with_reasons(song: Song, user: UserProfile) -> Tuple[float, List[str]]:
    """Return a song's score together with human-readable scoring reasons."""
    score = 0.0
    reasons: List[str] = []

    if song.genre == user.favorite_genre:
        score += 2.0
        reasons.append("genre match (+2.0)")

    if song.mood == user.favorite_mood:
        score += 1.0
        reasons.append("mood match (+1.0)")

    energy_difference = abs(song.energy - user.target_energy)
    energy_points = max(0.0, 1.0 - energy_difference)
    score += energy_points
    reasons.append(
        f"energy similarity (+{energy_points:.2f}) from {song.energy:.2f} vs target {user.target_energy:.2f}"
    )

    if user.likes_acoustic:
        acoustic_points = song.acousticness * 0.5
        score += acoustic_points
        reasons.append(
            f"acoustic preference fit (+{acoustic_points:.2f}) from acousticness {song.acousticness:.2f}"
        )
    else:
        acoustic_points = (1.0 - song.acousticness) * 0.5
        score += acoustic_points
        reasons.append(
            f"non-acoustic preference fit (+{acoustic_points:.2f}) from acousticness {song.acousticness:.2f}"
        )

    return score, reasons


def build_explanation(song: Song, user: UserProfile) -> str:
    """Convert scoring reasons into a single explanation string."""
    _, reasons = score_song_with_reasons(song, user)
    return "; ".join(reasons) + "."

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs: List[Dict] = []

    def parse_song_row(row: Dict[str, str]) -> Dict:
        """Convert one CSV row into a typed song dictionary."""
        return {
            "id": int(row["id"]),
            "title": row["title"],
            "artist": row["artist"],
            "genre": row["genre"],
            "mood": row["mood"],
            "energy": float(row["energy"]),
            "tempo_bpm": int(row["tempo_bpm"]),
            "valence": float(row["valence"]),
            "danceability": float(row["danceability"]),
            "acousticness": float(row["acousticness"]),
        }

    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            songs.append(parse_song_row(row))

    return songs

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    user = UserProfile(
        favorite_genre=user_prefs["favorite_genre"],
        favorite_mood=user_prefs["favorite_mood"],
        target_energy=user_prefs["target_energy"],
        likes_acoustic=user_prefs["likes_acoustic"],
    )

    scored_songs: List[Tuple[Dict, float, str]] = []
    for song_dict in songs:
        song = Song(
            id=song_dict["id"],
            title=song_dict["title"],
            artist=song_dict["artist"],
            genre=song_dict["genre"],
            mood=song_dict["mood"],
            energy=song_dict["energy"],
            tempo_bpm=song_dict["tempo_bpm"],
            valence=song_dict["valence"],
            danceability=song_dict["danceability"],
            acousticness=song_dict["acousticness"],
        )
        score, reasons = score_song_with_reasons(song, user)
        explanation = "; ".join(reasons) + "."
        scored_songs.append((song_dict, score, explanation))

    scored_songs.sort(key=lambda item: item[1], reverse=True)
    return scored_songs[:k]
