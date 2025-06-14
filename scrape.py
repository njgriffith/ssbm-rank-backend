import requests
import csv
import time

# --- Step 1: Get Event ID and Date from Slug ---
def get_event_id_and_date(slug, API_URL, HEADERS):
    query = """
    query GetEventId($slug: String!) {
      event(slug: $slug) {
        id
        name
        startAt
      }
    }
    """
    variables = { "slug": slug }
    response = requests.post(API_URL, json={"query": query, "variables": variables}, headers=HEADERS)
    data = response.json()

    if "errors" in data:
        raise Exception(f"GraphQL error: {data['errors']}")

    event = data["data"]["event"]
    event_id = event["id"]
    event_date = time.strftime('%Y-%m-%d', time.localtime(event["startAt"]))
    return event_id, event_date

# --- Step 2: Fetch Standings in Pages ---
def fetch_standings(event_id, per_page, url, api_headers):
    query = """
    query EventStandings($eventId: ID!, $page: Int!, $perPage: Int!) {
      event(id: $eventId) {
        standings(query: { page: $page, perPage: $perPage }) {
          pageInfo {
            totalPages
            total
          }
          nodes {
            placement
            entrant {
              name
              participants {
                user {
                  id
                  slug
                }
              }
            }
          }
        }
      }
    }
    """
    page = 1
    results = []

    while True:
        variables = {
            "eventId": event_id,
            "page": page,
            "perPage": per_page
        }
        response = requests.post(url, json={"query": query, "variables": variables}, headers=api_headers)
        data = response.json()

        if "errors" in data:
            raise Exception(f"GraphQL error on page {page}: {data['errors']}")

        standings = data["data"]["event"]["standings"]
        results.extend([
            {
                "placement": node["placement"],
                "entrant_name": node["entrant"]["name"],
                "user_id": node["entrant"]["participants"][0]["user"]["id"]
                if node["entrant"]["participants"] and node["entrant"]["participants"][0]["user"] else None
            } for node in standings["nodes"]
        ])

        if page >= standings["pageInfo"]["totalPages"]:
            break
        page += 1
        time.sleep(0.1)

    return results

# --- Step 3: Save to CSV ---
def save_to_csv(data, filename, event_id, event_date):
    for row in data:
        row["event_id"] = event_id
        row["event_date"] = event_date
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["placement", "entrant_name", "user_id", "event_id", "event_date"])
        writer.writeheader()
        writer.writerows(data)

# --- Main Scraper ---
def scrape(event_name):
    token = ''
    with open("assets/auth/start-gg-token.txt", "r") as f:
      token = f.readline().strip()
    SLUG = f"tournament/{event_name}/event/melee-singles"
    API_URL = "https://api.start.gg/gql/alpha"
    HEADERS = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    event_id, event_date = get_event_id_and_date(SLUG, API_URL, HEADERS)
    print(f"Got event: {event_name}, date: {event_date}")
    standings = fetch_standings(event_id, 100, API_URL, HEADERS)
    save_to_csv(standings, f"assets/results/{event_name}_standings.csv", event_id, event_date)
    print(f"Saved {len(standings)} entrants to {event_name}_standings.csv")
