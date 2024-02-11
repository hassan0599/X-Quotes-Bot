# X (Formerly Twitter) Bot with Flask and Redis

This project is an X bot built using Flask, Redis, and the X API. It allows users to authorize the bot to their X account, and it periodically posts tweets containing random quotes to the authorized user's timeline. Feel free to follow the bot on your X account [here](https://twitter.com/quotes_centre).

## Features

- Authorization with X OAuth2
- Periodic posting of tweets with random quotes and images of the authors!
- Refreshing OAuth2 tokens using Redis

## Files

1. **main.py**: Contains the main Flask application with routes for OAuth authorization and tweet posting.
2. **every_other_tweet.py**: Script for refreshing OAuth tokens and posting tweets.
3. **Procfile**: Specifies the command to run the Flask application using Gunicorn.
4. **requirements.txt**: Lists the Python packages required for the project.
5. **.github/workflows/actions.yml**: GitHub Actions workflow for scheduling the execution of every_other_tweet.py script.

## Setup

To set up this project locally, follow these steps:

1. Clone the repository.
2. Install the required Python packages listed in `requirements.txt`.
3. Set up environment variables for `CLIENT_ID`, `CLIENT_SECRET`, `REDIS_URL`, and `REDIRECT_URI`.
4. Run the Flask application using Gunicorn with the command specified in the Procfile.

## Hosting on Google Cloud Platform (GCP)

This X bot can be hosted on GCP using services like Google Cloud Run or Google Compute Engine. Here's a general guide to deploying it on GCP:

1. **Google Cloud Run**:
   - Containerize the Flask application using Docker.
   - Deploy the container to Cloud Run using the `gcloud run deploy` command.

2. **Google Compute Engine**:
   - Create a Compute Engine instance and set up a virtual machine with the required dependencies.
   - Deploy the Flask application on the Compute Engine instance.

Ensure you configure environment variables and access control settings appropriately, especially when deploying to a public cloud platform.

## Usage

1. Access the Flask application in your browser and authorize the X bot.
2. The bot will periodically post tweets with random quotes to your Twitter timeline.

## Contributing

Feel free to contribute to this project by opening issues or pull requests.

## License

This project is licensed under the [MIT License](https://opensource.org/license/mit/).
