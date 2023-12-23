import pandas as pd
import numpy as np
import streamlit as st
import cv2
import requests
from config import dictionaries as dic, lists as lst
#-----------------------------------------------------------------------------------------------------------------------
"""
def reveal_alcohol_types(ingredients):
    ing_text = str(ingredients)
    alc_list = list()

    for alc_type in dic.base_alcohols.keys():
        for brand in dic.base_alcohols[alc_type]:
            if str(alc_type) in ing_text.lower() or str(brand) in ing_text.lower():
                alc_list.append(alc_type)
    alc_list = sorted(list(set(alc_list)))
    if len(alc_list) > 0:
        return alc_list
    else:
        return ""

#-----------------------------------------------------------------------------------------------------------------------
def reveal_liqueurs(ingredients):
    ing_text = str(ingredients)
    liq_list = list()

    for liq_type in lst.liqueurs_list:
        if str(liq_type) in ing_text.lower():
            liq_list.append("liqueurs")
    liq_list = sorted(list(set(liq_list)))
    if len(liq_list) > 0:
        return liq_list
    else:
        return ""
"""
# ----------------------------------------------------------------------------------------------------------------------
def find_alcohol_types(ingredients):
    ingredients = map(str.lower, ingredients)
    alc_list = list()

    for ing in ingredients:
        for alc_type, brand in dic.base_alcohols.items():
            if alc_type == ing:
                alc_list.append(alc_type)
            if any(ing == brand_name for brand_name in brand):
                alc_list.append(alc_type)

    alc_list = sorted(list(set(alc_list)))
    return alc_list

#-----------------------------------------------------------------------------------------------------------------------
def find_liqueurs(ingredients):

    ingredients = map(str.lower, ingredients)
    liq_list = list()
    #print("ingredients:",ingredients)
    for ing in ingredients:
        for liq_type in lst.liqueurs_list:
            if liq_type == ing:
                liq_list.append("liquer")

    liq_list = sorted(list(set(liq_list)))
    return liq_list

#-----------------------------------------------------------------------------------------------------------------------
def replace_words(ingredients_list):
    ing_revised = [dic.correct_words.get(ing, ing) for ing in ingredients_list]
    return ing_revised

#-----------------------------------------------------------------------------------------------------------------------
def find_score(ingredients, ingredient_similarity_check, scoring_weights="arithmetical", report=False):

    #- manipulate ingredients
    ingredients_text = str(ingredients).lower()
    ingredients_list = [ing_.strip() for ing_ in ingredients_text.split(",") if not ing_.isspace() and ing_ != '']
    ingredients_list = replace_words(ingredients_list)

    if report:
        print(ingredients_list)

    ing_check_text = str(ingredient_similarity_check).lower()
    ing_check_list = [ing_.strip() for ing_ in ing_check_text.split(",") if not ing_.isspace() and ing_ != '']
    ing_check_list = replace_words(ing_check_list)

    if report:
        print(ing_check_list)

    #- score each ingredient match
    score1 = 0
    score2 = 0
    score3 = 0
    score4 = 0

    temp_ing_set = set()

    #- points for each exact match of ingredient
    for ing_exact in ingredients_list:

        if report:
            print("1 Exact Ing:", ing_exact)

        if ing_exact in ing_check_list:
            temp_ing_set.add(ing_exact)
            if report:
                print("Temporary ing set:", temp_ing_set)

            if scoring_weights == "arithmetical":
                if report:
                    print("2 Exact Ing:", ing_exact, " +60")
                score1 += 60
            elif scoring_weights == "equally":
                if report:
                    print("2 Exact Ing:", ing_exact, " +15")
                score1 += 15
            elif scoring_weights == "exact_match":
                if report:
                    print("2 Exact Ing:", ing_exact, " +60")
                score1 += 60

    #- points for each exact match of alcohol type
    for ing_exact in find_alcohol_types(ingredients_list):

        if report:
            print("Intersection count:", len(temp_ing_set.intersection({ing_exact})))

        if len(temp_ing_set.intersection({ing_exact})) == 0:

            if report:
                print("1 Alcohol:", ing_exact)

            if ing_exact in find_alcohol_types(ing_check_list):
                if scoring_weights == "arithmetical":
                    if report:
                        print("2 Alcohol:", ing_exact, " +30")
                    score2 += 30
                elif scoring_weights == "equally":
                    if report:
                        print("2 Alcohol:", ing_exact, " +15")
                    score2 += 15
                elif scoring_weights == "exact_match":
                    if report:
                        print("2 Alcohol:", ing_exact, " +60")
                    score2 += 60

                temp_ing_set.add(ing_exact)
                if report:
                    print("Temporary ing set:", temp_ing_set)

    #- points for each match of liqueur
    for ing_exact in find_liqueurs(ingredients_list):

        if report:
            print("Intersection count:", len(temp_ing_set.intersection({ing_exact})))

        if len(temp_ing_set.intersection({ing_exact})) == 0:

            if report:
                print("1 Liqueur:", ing_exact)

            if ing_exact in find_liqueurs(ing_check_list):
                if report:
                    print("2 Liqueur:", ing_exact)

                if scoring_weights == "arithmetical":
                    if report:
                        print("2 Liqueur:", ing_exact, " +15")
                    score3 += 15
                elif scoring_weights == "equally":
                    if report:
                        print("2 Liqueur:", ing_exact, " +15")
                    score3 += 15
                elif scoring_weights == "exact_match":
                    if report:
                        print("2 Liqueur:", ing_exact, " +10")
                    score3 += 10

                temp_ing_set.add(ing_exact)
                if report:
                    print("Temporary ing set:", temp_ing_set)

    #- points for word exact match of ingredient
    if report:
        print(sorted({ing_ for ing_ in ingredients_text.replace(","," ").split(" ") if not ing_.isspace() and ing_ != ''}))
        print(sorted({ing_ for ing_ in ing_check_text.replace(","," ").split(" ") if not ing_.isspace() and ing_ != ''}))

    for ing_word in {ing_ for ing_ in ingredients_text.replace(",", " ").split(" ") if not ing_.isspace() and ing_ != ''}:
        if ing_word in {ing_ for ing_ in ing_check_text.replace(",", " ").split(" ") if not ing_.isspace() and ing_ != ''}:

            if report:
                print("Intersection count:", len(temp_ing_set.intersection({ing_word})))

            if len(temp_ing_set.intersection({ing_word})) == 0:

                if scoring_weights == "arithmetical":
                    if report:
                        print("2 Word:", ing_word, " +5")
                    score4 += 5
                elif scoring_weights == "equally":
                    if report:
                        print("2 Word:", ing_word, " +15")
                    score4 += 15
                elif scoring_weights == "exact_match":
                    if report:
                        print("2 Word:", ing_word, " +5")
                    score4 += 5

                temp_ing_set.add(ing_word)
                if report:
                    print("Temporary ing set:", temp_ing_set)

    #- return total score
    final_score = score1 + score2 + score3 + score4

    if report:
        print("Final Score:", final_score)

    return final_score

#-----------------------------------------------------------------------------------------------------------------------
def style_image(image_path, border_radius=10, border_width=2, border_color='black'):
    st.markdown(
        f"""
        <style>
            .rounded-image-container {{
                overflow: hidden;
                border-radius: {border_radius}px;
                border: {border_width}px solid {border_color};
            }}
            .rounded-image {{
                width: 100%;
                height: auto;
                border-radius: {border_radius}px;
            }}
        </style>
        <div class="rounded-image-container">
            <img class="rounded-image" src="{image_path}" alt="Image">
        </div>
        """,
        unsafe_allow_html=True
    )

#-----------------------------------------------------------------------------------------------------------------------
def is_whole_number(value):
    return isinstance(value, float) and value.is_integer()

#-----------------------------------------------------------------------------------------------------------------------
def measurements_converter(from_name, to_name, amount):
    m = {"oz":1, "cl":3, "ml":30, "tblsp":2, "tsp":6, "shot":1.5, "cup":(1/8), "pint":(1/16), "quart":(1/32)}
    return m[to_name] / m[from_name] * amount

def load_img_and_resize(url, target_size=(400, 400), return_only_respond=False):

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    img_resp = requests.get(url, headers=headers, stream=True, allow_redirects=True)

    if return_only_respond:
        return img_resp

    if img_resp.status_code == 200:
        img = np.asarray(bytearray(img_resp.content), dtype="uint8")
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)

        resized_img = cv2.resize(img, target_size)
        resized_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)

        return resized_img
