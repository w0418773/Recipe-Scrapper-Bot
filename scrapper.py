import requests
from bs4 import BeautifulSoup

# Make Search Query
def GetSearchQuery(ingredient_List):

    # Create Query
    # EXAMPLE: https://www.allrecipes.com/search?q=eggs+ham+chives
    query = "https://www.allrecipes.com/search?q="

    # Counter for incrementing loop
    if(type(ingredient_List) is list): #Parameter is list
        x = 1

        for i in ingredient_List:
            if(x < len(ingredient_List)):
                query = query + i + "+"
            else:
                query = query + i

            x += 1
    else: # Parameter is string
        query = query + ingredient_List

    return query
# End SearchQuery

def GetUrls(IngredientList):
    url = GetSearchQuery(IngredientList)
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}

    r = requests.get(url, headers=headers)

    # Parsing the HTML, find each recipe on page
    soup = BeautifulSoup(r.content, 'html.parser')
    s = soup.find('div', {"id" : "mntl-search-results__list_1-0"})
    content = s.find_all("a", class_='comp mntl-card-list-card--extendable mntl-universal-card mntl-document-card mntl-card card card--no-image')

    url_List = []
    for i in content: #Loop through remove children, and grab HREF / create list of links
        i.clear()
        url_List.append(i.attrs["href"])
    
    return url_List

# End GetUrls

def GetRecipe(UrlList):
    RecipeList = []

    for i in UrlList:
        recipeURL = "https://www.allrecipes.com/recipe/"
        url = i
        if recipeURL in url:

            recipe = []
            headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}

            r = requests.get(url, headers=headers)
            soup = BeautifulSoup(r.content, 'html.parser')

            # Add URL
            recipe.append(url)

            # Get recipe name
            s = soup.find('h1', class_='article-heading text-headline-400')
            recipeName = s.get_text()
            recipe.append(recipeName)

            # Get Ingredients
            tmpIngredients = []

            s = soup.find('ul', class_='mm-recipes-structured-ingredients__list')
            for ingredient in s.find_all('li'):
                tmpIngredients.append(ingredient.get_text().strip())

            recipe.append(tmpIngredients) # Add ingredient list to array

            RecipeList.append(recipe)
    
    return RecipeList

# End GetRecipe