# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Real-world recommenders like Spotify or YouTube learn from behavior at scale — they track what millions of users skip, replay, or share, and surface content that similar users responded to, without ever being told why it worked. That approach (collaborative filtering) is powerful but opaque: it cannot explain a recommendation beyond "users like you also liked this." This version takes a different, more transparent path. It is a content-based recommender that scores each song by directly comparing its measurable features — genre, mood, energy, acousticness — against an explicit user preference profile. There is no learning from past behavior, no hidden latent space, and no black box: every score is a sum of human-readable terms, so it is always possible to trace exactly why a song ranked first or last. The trade-off is that the system can only match what the user already knows they want; it will never surprise them with something outside their stated profile. That limitation is the honest cost of keeping the logic fully inspectable.

### `Song` features

| Field | Type | Role |
|---|---|---|
| `id` | `int` | Unique identifier — not used in scoring |
| `title` | `str` | Display only — not used in scoring |
| `artist` | `str` | Display only — not used in scoring |
| `genre` | `str` | Categorical — matched against user preference |
| `mood` | `str` | Categorical — matched against user preference |
| `energy` | `float [0,1]` | Numerical — proximity scored against `target_energy` |
| `tempo_bpm` | `float` | Numerical — available but not yet wired to a user preference |
| `valence` | `float [0,1]` | Numerical — available but not yet wired to a user preference |
| `danceability` | `float [0,1]` | Numerical — available but not yet wired to a user preference |
| `acousticness` | `float [0,1]` | Numerical — direction scored against `likes_acoustic` |

### `UserProfile` features

| Field | Type | What it matches in `Song` |
|---|---|---|
| `favorite_genre` | `str` | `song.genre` — exact match |
| `favorite_mood` | `str` | `song.mood` — exact match |
| `target_energy` | `float [0,1]` | `song.energy` — proximity score |
| `likes_acoustic` | `bool` | `song.acousticness` — directional score |

> **Gap to note:** `tempo_bpm`, `valence`, and `danceability` exist in the song data but have no corresponding `UserProfile` field. The scoring rule currently ignores them. Either extend `UserProfile` to cover them, or document the omission as a known limitation in the model card.

---

## How The System Works

Explain your design in plain language.

My system loads a catalog of songs, builds a numeric score for each song by comparing its features to what a user prefers, sorts by score, and hands back the best matches — with a plain-English explanation of why each one was chosen.

The specific taste profile I use for comparisons is a dictionary of target feature values for a listener who wants energetic, positive music for workouts or commuting:

```python
user_prefs = {
    "favorite_genre": "pop",
    "favorite_mood": "happy",
    "target_energy": 0.80,
    "likes_acoustic": False,
}
```

That means the recommender should favor upbeat pop songs with happy moods, strong energy, and low acousticness.

### Plan

The recommender uses one user profile plus the song catalog in `data/songs.csv`. It reads every song, checks how well that song matches the user's preferred genre, preferred mood, target energy, and acoustic preference, and then assigns a total score. After every song has been scored, the system sorts the list from highest score to lowest score and returns the top `k` songs as recommendations.

### Algorithm Recipe

For each song in the CSV:

1. Start with a score of `0.0`.
2. Add `+2.0` points if the song's genre exactly matches the user's favorite genre.
3. Add `+1.0` point if the song's mood exactly matches the user's favorite mood.
4. Add energy similarity points using `1.0 - abs(song.energy - user.target_energy)`, with a minimum of `0.0`.
5. Add up to `+0.5` points for acoustic fit:
   - if the user likes acoustic music, reward higher `acousticness`
   - if the user does not like acoustic music, reward lower `acousticness`
6. Save the song, its score, and a short explanation.
7. Sort all scored songs in descending order.
8. Return the top `k` songs.

This recipe gives genre the strongest influence, mood the next strongest influence, and then uses energy and acousticness as tie-breakers that fine-tune the ranking.

### Potential Biases

This system might over-prioritize genre, ignoring songs from other genres that still match the user's mood and energy really well. It also depends on exact labels like `"afrobeat"` or `"uplifting"`, so songs that are similar in feel but tagged differently may be ranked too low. Because the dataset is small and the algorithm only uses a few features, the recommender may also reflect the limits and biases of the catalog more than the full range of a listener's taste.

### Data Flow Map

Input (`user_prefs`) -> Process (`recommend_songs` loops through every song in `songs.csv` and scores each one) -> Output (songs sorted by score and trimmed to the top `k` recommendations).

<img width="8192" height="916" alt="Song Recommendation Scoring-2026-04-13-215243" src="https://github.com/user-attachments/assets/25590f26-bb4c-4dda-be6e-c07b25ebaedd" />


The diagram matches the code path for a single song: one CSV row is loaded, turned into a `Song`, scored against the user profile, packaged with its explanation, added to the scored list, and only then compared against the other songs during sorting.

### Terminal Output Example

Running `python -m src.main` with the default `pop/happy` profile produces results that match the scoring recipe: `Sunrise City` ranks first because it matches both genre and mood while landing very close to the target energy, and `Gym Hero` ranks next because it shares the pop genre and also scores well on energy and low acousticness.

![Terminal screenshot of recommendation output](assets/recommendations_terminal.png<img width="874" height="593" alt="Screenshot 2026-04-13 at 23 33 58" src="https://github.com/user-attachments/assets/1d055e01-8f04-4b80-85ef-c20e6265deb6" />
)

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"
