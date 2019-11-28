from datetime import date as date_obj

from flask import request
from flask import abort, redirect, render_template, url_for
import requests

from src.blueprint import search
from src.core import api
from src.core.filters import create_api_date
from src.core.form import PromptSearchForm


@search.route("/", methods=["GET"])
def index():
    abort(404)
    render_opts = {
        "form": PromptSearchForm()
    }
    return render_template("search/search.html", **render_opts)


@search.route("/results", methods=["GET"])
def query_search():
    abort(404)
    # We got a valid form submission
    search_form = PromptSearchForm()
    query = request.args.get("query").strip()

    try:
        # We recieved an exact (and valid) date, redirect to it
        date_obj.fromisoformat(query)  # noqa
        return redirect(url_for("root.view_date", date=query))

    # We got a word or partial word to search
    except ValueError:
        # Populate the input with the search term (so... it's a sticky form)
        search_form.query.data = query
        render_opts = {"form": search_form}

        # Connect to the API to search
        try:
            response = api.get("search", params={"prompt": query})

        # The search was not successful
        except requests.exceptions.HTTPError:
            render_opts["query"] = query
            render_opts["total"] = 0
            return render_template("search/results.html", **render_opts)

        # We got many search results
        if response["total"] >= 2:
            render_opts.update(response)
            return render_template("search/results.html", **render_opts)

        # We got a single response back, go directly to the prompt
        elif response["total"] == 1:
            date = create_api_date(response["prompts"][0]["date"])
            date = date.strftime("%Y-%m-%d")
            return redirect(url_for("root.view_date", date=date))

        # No search results were returned
        else:
            render_opts.update(response)
            return render_template("search/results.html", **render_opts)