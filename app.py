from flask import Flask, render_template, request
# render template - it is use to render HTML web templates.
# request - it is used to access the incoming request data.
import requests
from urllib.parse import unquote  # The Unquote method returns the input string with no quotation marks at the beginning and at the end of the string
# The urllib. parse module provides functions for manipulating URLs and their component parts, to either break them down or build them up.
# Craete the flask app
app = Flask(__name__)

#Replace with your Spoonacular API key
API_KEY = '4155ece92bf44eaba518b552ac76ce62'

@app.route('/home', methods=['GET'])
def home():
    return render_template('index.html', recipes=[], search_query='')

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        #If a form is submitted
        query= request.form.get('search_query','')
        # Perform a search for recipes with the given query
        recipes=search_recipes(query)
        return render_template('index.html', recipes=recipes, search_query=query)
    #if it's a GET request or no form submitted
    search_query = request.args.get('search_query','')
    decoded_search_query = unquote(search_query)
    recipes = search_recipes(decoded_search_query)
    return render_template('index.html', recipes = recipes, search_query = decoded_search_query)

# function to search for recipes based on the provided query
def search_recipes(query):
    url = f'https://api.spoonacular.com/recipes/complexSearch'
    params = {
        'apiKey': API_KEY,
        'query': query,
        'number': 10,
        'instructionsRequired': True,
        'addRecipeInformation': True,
        'fillIngredients': True,
    }

    # Send a GET request to the Spoonacular API with the query parameters
    response = requests.get(url, params=params)
    # If the API call is successful
    if response.status_code == 200:
        data = response.json()
        return data['results']
    # if the API not successful
    return []

# Route to view a specific recipe with a given recipe ID
@app.route('/recipe/<int:recipe_id>')
def view_recipe(recipe_id):
    # Get the search query from the URL query parameters
    search_query = request.args.get('search_query','')
    # Build the URL to get information about the specific recipe ID from Spoonacular API
    url = f'https://api.spoonacular.com/recipes/{recipe_id}/information'
    params = {
        'apiKey' : API_KEY
    }

    # Send a GET request to the Spoonacular API to get the recipe information
    response = requests.get(url, params = params)
    if response.status_code == 200:
        recipe = response.json()
        return render_template('view_recipe.html', recipe=recipe, search_query = search_query)
    return "Recipe not found", 404

# Run the app in debug mode if executed directly
if __name__ == '__main__':
    app.run(debug=True)








 

