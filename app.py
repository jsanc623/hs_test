from flask import Flask
from dotenv import load_dotenv

from api import get, post
from data import transform

app = Flask(__name__)
load_dotenv()


@app.route('/')
def main():
    response = get()
    if response.status_code != 200:
        return {"status": response.status_code, "msg": response.text}

    transformed_dataset = transform(response.json())
    post_response = post(transformed_dataset)

    return {"1status": post_response.status_code, "1msg": post_response.json(), "data": transformed_dataset}


if __name__ == '__main__':
    app.run()
