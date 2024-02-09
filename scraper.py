import datetime
import requests

# Get today's date
today = datetime.datetime.now()
date = today.strftime('%m/%d')

# Wikipedia API endpoint
url = 'https://api.wikimedia.org/feed/v1/wikipedia/en/onthisday/all/' + date

# Headers for the request
headers = {
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI1NmJlNmRjMTE0MDhiYmRlMTRiOWVmMWU0MTY2YTg0YSIsImp0aSI6IjI0NTliYjMzNzRlNzQ3NTk1YWVjZWY2NDAxMzU5YTNmZTA3NGYzZTAwNDRhZDJhMTQzNTYzZjNhZjg3ZjZjOGQwNTM3NTgxMzgwODU0NjNhIiwiaWF0IjoxNzA3NDg1OTAyLjM5Nzk0NiwibmJmIjoxNzA3NDg1OTAyLjM5Nzk1LCJleHAiOjMzMjY0Mzk0NzAyLjM5NTQ4LCJzdWIiOiI3NDkzNTQ2MiIsImlzcyI6Imh0dHBzOi8vbWV0YS53aWtpbWVkaWEub3JnIiwicmF0ZWxpbWl0Ijp7InJlcXVlc3RzX3Blcl91bml0Ijo1MDAwLCJ1bml0IjoiSE9VUiJ9LCJzY29wZXMiOlsiYmFzaWMiXX0.aamee_SW6ePpqTw7j65UGAciADVIkEGV9yF7mNISOG0qzQvAtuqe7rfLlH6_Mo7t8KAoM_OU8apFGPI6Z8aNAsxjOQaOCxOKxMOis3KbCt7qSaHpOX7apRxJOUlP6DpckJ-HSwkJejlTgdBlt1wG9HLyn_OJGI-Bk2MIopV7EshKs56oC6RQM7Bu5fXEPNvTrLufehPMobT7vtBfrQKiXzt2bLSVTIf-HpNl4NfEgMZuxScLNEWLIauBPpmOomOMcZD832R8D-9XULz-7BTJYZRuyNGvUOwdKIgiB-WULPJVpHdbZxlW3SStvZODO6Yzt7CGqXis09pxW8TLhI63wMx4VkPK6lwS_dv8f0sz-XraWCfF7eM1LI0Tcy7NyrvxDwnTHGwQnJ2m8xkORFvJSHCUBaHk-uA0fbOzOIv6_4bwpIYlipbWPR_BBK7WoytB5LmpfiImtDwk5zsx9OK1rXHhEo4y9w5XW4N7N_tT0YZ7rfTV8_c8CHF0mDJe0X4zS0KKxHBHoEVWS6YhKu2pqnTPTl4c-l01ARJ1DpHuCjY-xJKYPEO-2wiht3uGOGAHrKIF8cDqPq2TQ7JKMwA_J8XyefRVxDrVeHKjKPR-uVB2Cidd9-2z0GPi6GQYQ14blRt232qS88c7vbsrJS_SIPyvb3HAzorgdCB8ZNKiUv4',  # Replace with your access token
    'User-Agent': 'TimeTravelPakistan umairnawaz184@gmail.com'  # Replace with your app name and contact
}

# Send a GET request to the Wikipedia API
response = requests.get(url, headers=headers)

# Parse the JSON response
data = response.json()

# Print the data
for section in ['events', 'births', 'deaths']:
    print(f"## {section.capitalize()}")
    print("\n")
    for item in data[section]:
        print(f"- {item['year']}: {item['text']}")
    print("\n")
