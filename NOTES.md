# First Steps [5 min in]

To start with the project I decided to create most of the folder architecture and src files before starting to code anything, for this I've based myself on previous projects that had a similar architecture, but on a larger scale. Then I went to set environment variables and other config settings, just as a placeholder for now. In this step I also created a project in Google AI labs to get the API_KEY.

# File management [30 min in]

The next step for me is to process the data into plain text, for this I use the pathlib to get the .txt contents on standard UTF-8.

# Schemas [1 hr in]

I wrote the output schema using pydantic so the model had a more readable structure as a json format, at the same time I wrote the prompt that's gonna be used for the model and got the criteria from the brief.md, validating the input from the model using Literals. For this I used Gemini Flash model to create a boilerplate of the prompt template and tuned it accordingly to what was required.

# Model [1 hr 30 mins in]

## The Fun Part

For the model I'll be using Gemini from Google's AI Lab. To be honest my first thought was to run a local ollama server with a qwen3:8b but for this exercise I preferred to use an actual cloud model in the end.

I had to test multiple models from Google AI Lab since I wasn't familiarized with the tool, but after looking through a list of all available models I selected (in this case for testing), gemini-2.5-flash, it was one of the cheapest options (free tier, X amount of tokens and 100 calls)

To ensure reliability during processing, I implemented a loop with exception handling that gracefully recovers from network glitches or rate limits

# Testing [2 hrs 45 mins in]

For the testing I compared every point from the AI-generated evaluations against the expected human evaluation for each call. I reviewed the disagreements criterion by criterion to identify where the model's interpretation differed from the rubric.

# Dockerization [3 hrs 20 mins in]

This was the part where I got a bit of trouble because I had to change the routing to the files I had to those relative to the app container. But other than that (and some error handling from the .toml) it went great!

# Everything else [3 hrs 40 mins in]

The last 20 minutes I've used to write the findings, manually analyze the evaluations made by the model and the human side, etc.

# What would I do with one more day

With more time to develop the application I would:

- Probably add an interface or at least more prints that would guide the user, and that allowed to check and override the scores if required.
- Test the program with bigger batches of transcripts / stress testing.
- Test multiple models to see which one fits the best.
- Train the model to get better results, being careful of not overfitting it (this would probably take some time though).
- Clean the code a bit, so I could move the writing of results to a function on the file_utils.
- Give it a COT type of structure so it would rethink what it is writing with its own answer, but checking that it doesn't use too much tokens.
- If it's gonna be a tool used by the employees I would try to add some logging of how many tokens are being used, to keep track of the expense.
