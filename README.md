# soccer_results_scraper

A very simple web app built with Python and Flask that delivers soccer betting results taken from the website **livescore.cz**
Bet results are:

**_final_result_**: can be 1,X or 2
**_total_**: can be over or under

## Endpoints

### GET: /

returns a json like

[
{
"home": "Argentina",
"away": "France,
"final_result": "X",
"total": "O"
}
]
