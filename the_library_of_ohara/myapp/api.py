import requests

"""Anime"""

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


def fetch_anime_list(page=1, per_page=10):
    query = """
    query ($page: Int, $perPage: Int) {
        Page(page: $page, perPage: $perPage) {
            pageInfo {
                total
                currentPage
                lastPage
                hasNextPage
                perPage
            }
            media(type: ANIME) {
                id
                title {
                    romaji
                    english
                }
                coverImage {
                    large
                }
            }
        }
    }
    """

    variables = {
        "page": page,
        "perPage": per_page
    }

    url = 'https://graphql.anilist.co'

    # Make the HTTP Api request
    response = requests.post(url, json={'query': query, 'variables': variables})

    if response.status_code == 200:
        return response.json().get('data').get('Page')
    else:
        return None


"""Manga"""

def fetch_manga_by_id(manga_id):
    query = """
    query ($id: Int) {
        Media(id: $id, type: MANGA) {
            id
            title {
                romaji
                english
                native
            }
            coverImage {
                large
            }
            description
            genres
            chapters
            status
            startDate {
                year
                month
                day
            }
            endDate {
                year
                month
                day
            }
            staff {
                edges {
                    node {
                        name {
                            full
                        }
                    }
                    role
                }
            }
            averageScore
        }
    }
    """
    variables = {
        "id": manga_id
    }
    url = 'https://graphql.anilist.co'
    response = requests.post(url, json={'query': query, 'variables': variables})

    if response.status_code == 200:
        return response.json().get('data').get('Media')
    else:
        return None


def fetch_manga_list(page=1, per_page=10):
    query = """
    query ($page: Int, $perPage: Int) {
        Page(page: $page, perPage: $perPage) {
            pageInfo {
                total
                currentPage
                lastPage
                hasNextPage
                perPage
            }
            media(type: MANGA) {
                id
                title {
                    romaji
                    english
                }
                coverImage {
                    large
                }
            }
        }
    }
    """

    variables = {
        "page": page,
        "perPage": per_page
    }

    url = 'https://graphql.anilist.co'

    # Make the HTTP Api request
    response = requests.post(url, json={'query': query, 'variables': variables})

    if response.status_code == 200:
        return response.json().get('data').get('Page')
    else:
        return None