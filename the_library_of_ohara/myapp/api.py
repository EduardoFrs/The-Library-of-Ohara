import requests

def fetch_anime_by_id(anime_id):
    query = """
    query ($id: Int) {
        Media(id: $id, type: ANIME) {
            id
            title {
                romaji
                english
                native
            }
            episodes
            status
            description
            averageScore
            genres
            coverImage {
                large
            }
        }
    }
    """

    variables = {
        "id": anime_id
    }

    url = 'https://graphql.anilist.co'

    # Make the HTTP Api request
    response = requests.post(url, json={'query': query, 'variables': variables})
    if response.status_code == 200:
        return response.json().get('data').get('Media')
    else:
        return None