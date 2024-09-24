from flask import Flask, request, render_template, session
from stories import Story

app = Flask(__name__)
app.secret_key = "your_secret_key"


@app.route("/")
def home_page():
    """Shows Homepage with the story choices for a user"""
    return render_template("home.html")


@app.route("/form")
def show_form():
    """Shows form with input choices for user."""
    story_choice = request.args["story"]
    if story_choice == "past":
        story = Story(
            ["place", "noun", "verb", "adjective", "plural_noun"],
            """Once upon a time in a long-ago {place}, there lived a large {adjective} {noun}. It loved to {verb} {plural_noun}.""",
        )
    elif story_choice == "present":
        story = Story(
            ["place", "noun", "verb", "adjective", "plural_noun"],
            """There is this {place}, where there is a medium sized {adjective} {noun}. It loves to {verb} {plural_noun}.""",
        )
    elif story_choice == "future":
        story = Story(
            ["place", "noun", "verb", "adjective", "plural_noun"],
            """In this futuristic {place}, there will be a small {adjective} {noun}. It is going to love to {verb} {plural_noun}.""",
        )

    session["story_prompts"] = story.prompts
    session["story_template"] = story.template

    return render_template("form.html", story_choice=story_choice, story=story)


@app.route("/story")
def show_story():
    """Shows rendered story for user"""

    story_params = request.args.to_dict()
    prompts = session.get("story_prompts")
    template = session.get("story_template")

    story = Story(prompts, template)

    generated_story = story.generate(story_params)

    return render_template(
        "story.html",
        story=generated_story,
    )
