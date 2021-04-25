from flask import Flask
import requests
import math

PAGESIZE = 100


def get_data_dictionary(username):
    response1 = requests.get("https://api.github.com/users/{0}".format(username))
    num_of_repos = response1.json()["public_repos"]

    server_response = {"repositories": {},
                       "stars_total": 0}

    for i in range(math.ceil((num_of_repos / PAGESIZE)) + 1):
        response = requests.get("https://api.github.com/users/{0}/repos".format(username),
                                params={"per_page": PAGESIZE, "page": i})

        response_list = response.json()

        for repository in response_list:
            server_response["repositories"][repository["name"]] = repository["stargazers_count"]
            server_response["stars_total"] += repository["stargazers_count"]

    return server_response


app = Flask(__name__)


@app.route('/')
def index():
    return "get repositories: '/username' <br>get total number of stars: '/stars/username'"


@app.route('/<name>')
def get_repos(name):
    response = requests.get("https://api.github.com/users/{0}".format(name))

    if response.status_code != 200:
        return "No such user"

    return {"repositories": get_data_dictionary(name)["repositories"]}

@app.route('/stars/<name>')
def get_stars(name):
    response = requests.get("https://api.github.com/users/{0}".format(name))

    if response.status_code != 200:
        return "No such user"
    
    return {"stars_total": get_data_dictionary(name)["stars_total"]}

if __name__ == "__main__":
    app.run(debug=True)
