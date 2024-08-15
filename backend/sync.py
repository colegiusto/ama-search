import requests
import pandas

id = "1i2tmn7L-nlqOz0i-O1MVoOg6kafe9gC45VkaXs0LxMA"

def update_sheet(sid):
    uri = f"https://docs.google.com/spreadsheets/d/{id}/export?format=csv"
    r = requests.get(uri)
    if r.status_code == 200:
        with open("data.csv", "wb+") as f:
            f.write(r.content)

if __name__ == "__main__":
    update_sheet(id)