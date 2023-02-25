# Youtube-navigator

Youtube Navigator is an chrome extension that provides personalized summaries for users directly on YouTube.

## Instructions

To run this code you will need to create OpenAI API key here <https://platform.openai.com/account/api-keys>

After this to run this code, follow these steps:

1. Create an `.env` file in the DjangoServer directory and put OpenAI API key in the `OPENAI_API_KEY` environment variable.

2. Run command `pip install -r requirements.txt` in `DjangoServer` directory to install necessary packages.

3. Start the server by running the following command in the `DjangoServer` directory: `python manage.py runserver localhost:4000`

4. After this go to chrome://extensions/

5. Toggle "Developer mode" on in the upper right corner of the screen.

6. Click the "Load unpacked" button in the upper left corner.

7. Select the `build` directory and click "Open".

8. Enjoy!

## Limitation

Right now videoID of youtube video is hardcoded to this video <https://www.youtube.com/watch?v=0z49WJGAdyY&ab_channel=BrandonCarter>
