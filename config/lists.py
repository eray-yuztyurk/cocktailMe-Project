from config import dictionaries as dic
import nltk
from nltk.corpus import stopwords
#-----------------------------------------------------------------------------------------------------------------------
# apply nltk stopwords
nltk.download("stopwords")
stop_words = set(stopwords.words("english"))

remove_words = list(stop_words)
#-----------------------------------------------------------------------------------------------------------------------
#- prepare alcohol types lists
brandy_types = ["american brandy", "apple brandy", "apricot brandy", "armagnac", "brandy de jerez", "calvados",
                "cherry brandy", "chilean pisco", "cognac", "french brandy", "grappa", "italian brandy", "pear brandy",
                "peach brandy", "peruvian pisco", "plum brandy", "pisco", "singani", "spanish brandy"]
gin_types = ["american gin", "australian gin", "barrel-aged gin", "botanical gin", "cask-aged gin", "flavored gin",
             "genever", "gin liqueur", "holland gin", "irish gin", "london dry gin", "london gin", "navy strength gin",
             "new western or contemporary gin", "old tom gin", "organic gin", "plymouth gin", "sloe gin", "spanish gin"]
rum_types = ["aged rum", "agricole rum", "cachaça", "dark rum", "flavored rum", "gold rum", "honey rum", "navy rum",
             "overproof rum", "premium or ultra-premium rum", "rhum traditionnel", "rum cream", "rum liqueur",
             "spiced rum", "white rum"]
tequila_types = ["100% agave tequila", "aged tequila", "anejo tequila", "bacanora", "blanco tequila",
                 "extra añejo tequila", "flavored tequila", "infused tequila", "joven tequila", "mezcal",
                 "mezcal joven", "mixto tequila", "organic tequila", "raicilla", "reposado tequila", "sotol",
                 "silver tequila", "white tequila"]
vodka_types = ["blueberry vodka", "cake vodka", "caramel vodka", "cherry vodka", "chocolate vodka", "citrus vodka",
               "coconut vodka", "cucumber vodka", "espresso vodka", "flavored vodka", "fruit-infused vodka",
               "ginger vodka", "herb-infused vodka", "lemon vodka", "lime vodka", "melon vodka", "mint vodka",
               "orange vodka", "pepper vodka", "peppermint vodka", "plain vodka", "raspberry vodka", "rose vodka",
               "strawberry vodka", "tea-infused vodka", "vanilla vodka", "whipped cream vodka"]
whiskey_types = ["american whiskey", "blended scotch", "blended whiskey", "bourbon", "canadian whisky",
                 "cask strength whiskey", "corn whiskey", "craft whiskey", "flavored whiskey", "honey whiskey",
                 "irish whiskey", "islay scotch", "japanese whisky", "lowland scotch", "maple whiskey", "malt whiskey",
                 "non-peaty scotch", "peaty scotch", "rye", "rye malt whiskey", "rye whiskey", "scotch",
                 "scotch whisky", "single cask whiskey", "single malt scotch", "single pot still whiskey",
                 "speyside scotch", "straight whiskey", "tennessee whiskey", "wheat whiskey"]

#-----------------------------------------------------------------------------------------------------------------------
#- combine alcohol types lists
for value in brandy_types:
    for old_word, new_word in dic.correct_words.items():
        dic.base_alcohols["brandy"].append(value.replace(old_word, new_word))

for value in gin_types:
    for old_word, new_word in dic.correct_words.items():
        dic.base_alcohols["gin"].append(value.replace(old_word, new_word))

for value in rum_types:
    for old_word, new_word in dic.correct_words.items():
        dic.base_alcohols["rum"].append(value.replace(old_word, new_word))

for value in tequila_types:
    for old_word, new_word in dic.correct_words.items():
        dic.base_alcohols["tequila"].append(value.replace(old_word, new_word))

for value in vodka_types:
    for old_word, new_word in dic.correct_words.items():
        dic.base_alcohols["vodka"].append(value.replace(old_word, new_word))

for value in whiskey_types:
    for old_word, new_word in dic.correct_words.items():
        dic.base_alcohols["whiskey"].append(value.replace(old_word, new_word))

#-----------------------------------------------------------------------------------------------------------------------
# Creating base_alcohols_list
base_alcohols_list = []

for alc, brands in dic.base_alcohols.items():
    for brand in brands:
        if alc not in base_alcohols_list:
            base_alcohols_list.append(alc)
        if brand not in base_alcohols_list:
            base_alcohols_list.append(brand)

#-----------------------------------------------------------------------------------------------------------------------
# Creating liqueurs_list
liqueurs_list = []

for liquor, brands in dic.liqueurs.items():
    for brand in brands:
        if liquor not in liqueurs_list:
            liqueurs_list.append(liquor)
        if brand not in liqueurs_list:
            liqueurs_list.append(brand)

#-----------------------------------------------------------------------------------------------------------------------
# Creating wine_list
wine_list = []

for wine, brands in dic.wines.items():
    for brand in brands:
        if wine not in wine_list:
            wine_list.append(wine)
        if brand not in wine_list:
            wine_list.append(brand)

#-----------------------------------------------------------------------------------------------------------------------
# Creating beer_list
beer_list = []

for beer, brands in dic.beers.items():
    for brand in brands:
        if brand not in beer_list:
            beer_list.append(brand)

#-----------------------------------------------------------------------------------------------------------------------
# Create Final Alcohol List
alcohol_list = dic.base_alcohols
alcohol_list["wine"] = wine_list
alcohol_list["beer"] = beer_list

#-----------------------------------------------------------------------------------------------------------------------
#- measurements types list
measurement_types = ["oz", "cl", "ml", "tblsp", "tsp", "shot", "cup", "pint", "quart"]