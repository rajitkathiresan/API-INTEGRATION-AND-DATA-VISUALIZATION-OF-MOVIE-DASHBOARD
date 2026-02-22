import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

API_KEY = "0a59acacdedfe3ab79df33feb306d7d4"

BASE_URL = "https://api.themoviedb.org/3"

# Fetch Top Rated Movies
url = f"{BASE_URL}/movie/top_rated?api_key={API_KEY}&language=en-US&page=1"
response = requests.get(url)
data = response.json()

movies = data['results']

# Create DataFrame
df = pd.DataFrame(movies)[['title', 'vote_average', 'release_date', 'genre_ids']]

# Convert release year
df['release_year'] = pd.to_datetime(df['release_date']).dt.year

# -------------------------------
# Fetch Genre Mapping
# -------------------------------
genre_url = f"{BASE_URL}/genre/movie/list?api_key={API_KEY}&language=en-US"
genre_data = requests.get(genre_url).json()

genre_dict = {g['id']: g['name'] for g in genre_data['genres']}

# Count genre frequency
genre_count = {}

for genres in df['genre_ids']:
    for g in genres:
        genre_name = genre_dict.get(g, "Unknown")
        genre_count[genre_name] = genre_count.get(genre_name, 0) + 1

genre_df = pd.DataFrame(genre_count.items(), columns=['Genre', 'Count']).sort_values(by='Count', ascending=False)

# -------------------------------
# Visualization Dashboard
# -------------------------------
plt.figure(figsize=(14,6))

# Scatter Plot: Ratings vs Release Year
plt.subplot(1,2,1)
sns.scatterplot(x=df['release_year'], y=df['vote_average'])
plt.title("Movie Ratings vs Release Year")
plt.xlabel("Release Year")
plt.ylabel("Rating")

# Bar Chart: Genre Popularity
plt.subplot(1,2,2)
sns.barplot(x='Count', y='Genre', data=genre_df.head(10))
plt.title("Top 10 Movie Genres")

plt.tight_layout()
plt.show()
