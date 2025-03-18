import os
import csv
import requests
from bs4 import BeautifulSoup

# Get the SoundCloud Artist URL from GitHub Actions input
SOUNDCLOUD_ARTIST_URL = os.getenv("SOUNDCLOUD_ARTIST_URL")


def scrape_soundcloud_songs(artist_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }
    
    response = requests.get(artist_url, headers=headers)
    if response.status_code != 200:
        print("Failed to fetch SoundCloud page")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    # Extract song data (this may require adjustments if SoundCloud's HTML structure changes)
    songs = []
    for track in soup.find_all("article", class_="soundList__item"):
        title_tag = track.find("a", class_="soundTitle__title")
        play_count_tag = track.find("span", class_="sc-ministats")

        if title_tag and play_count_tag:
            song_name = title_tag.text.strip()
            song_plays = play_count_tag.text.strip()
            songs.append((song_name, song_plays))

    return songs


def main():
    if not SOUNDCLOUD_ARTIST_URL:
        print("Error: SoundCloud artist URL is required.")
        return

    csv_filename = "soundcloud_song_play_data.csv"

    with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Artist Name", "Song Name", "Song Plays"])

        # Scrape SoundCloud song play data
        songs = scrape_soundcloud_songs(SOUNDCLOUD_ARTIST_URL)

        for song_name, song_plays in songs:
            writer.writerow(["SoundCloud Artist", song_name, song_plays])

    print(f"CSV file '{csv_filename}' generated successfully!")


if __name__ == "__main__":
    main()
