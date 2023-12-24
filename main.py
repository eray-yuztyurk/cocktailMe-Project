########################################################################################################################
#-------------- IMPORT LIBRARIES AND SOME SHOWING SETTING -------------------------------------------------------------#
########################################################################################################################
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from src.utils import find_score, measurements_converter, load_img_and_resize
from config.dictionaries import correct_words
from config.lists import remove_words
import config.lists as lst
import time
########################################################################################################################
#-------------- STREAMLIT GENERAL PAGE SETTINGS -----------------------------------------------------------------------#
########################################################################################################################
st.set_page_config(page_title="cocktailMe", page_icon="🍹", layout="wide")
style = """
<style>
    body {
        background-image: url('file://img/bg_img_1.jpg');
        background-size: cover;
    }
    img {
        border-radius: 10px;
        border: 1px solid #808080;
        padding: 3px;
        transition: transform 0.3s ease;
    }
    img:hover {
        transform: scale(1.05);
    }
</style>
"""

st.markdown(style, unsafe_allow_html=True)

logo = st.container(border=True)
logo.image("img/cocktailMe_logo.png", use_column_width=100)
welcome, cocktail_finder, measurement = st.tabs(["Welcome", "Cocktail Finder", "Measurements"])

########################################################################################################################
#-------------- READ FINAL DATASETS  ----------------------------------------------------------------------------------#
########################################################################################################################
@st.cache_data
def load_data():
    cocktails_df = pd.read_csv("data/cocktails_df_final.csv")
    cocktails_df.drop(cocktails_df.columns[0], axis=1, inplace=True)
    cocktails_df.drop(309, axis=0, inplace=True)
    return cocktails_df

cocktails_df = load_data()

########################################################################################################################
#-------------- WELCOME SECTION ---------------------------------------------------------------------------------------#
########################################################################################################################
#- containers
left_side, right_side = welcome.columns([2, 2])
left_container = left_side.container(border=True)
right_container = right_side.container(border=True)

#- containers' contents
welcome_text = "Welcome to :rainbow[cocktail Me]! ✨"
welcome_text1 = """

Indulge in a warm greeting and step into the world of Cocktail Me — your personal haven guided by a friendly AI Bartender! 🍹🤖"""
welcome_text2 = """

Embark on a delightful journey where the art of mixology meets the magic of innovation."""
welcome_text3 = """🌈 Your virtual cocktail companion is here to transform your drink decisions into moments of effortless joy."""

welcome_text4 = """

Let's explore a world where every sip is a celebration, and each beverage choice becomes a breeze. Join me in making your moments extraordinary! 🍹🎉"""

welcome_text5 = """

Cheers to the perfect blend of taste, creativity, and unforgettable experiences! 🥂"""

img = right_container.empty()
welcome_text_all = left_container.empty()
text = ""
for word in welcome_text.split():
    text += word + " "
    welcome_text_all.subheader(text)
    time.sleep(0.01)
time.sleep(0.2)
img.image("img/ai/ai_waits2.jpg", use_column_width=True)
left_container.divider()

welcome_text_all1 = left_container.empty()
text = ""
for word in welcome_text1.split():
    text += word + " "
    welcome_text_all1.markdown(text)
    time.sleep(0.01)
time.sleep(0.2)

welcome_text_all2 = left_container.empty()
text = ""
for word in welcome_text2.split():
    text += word + " "
    welcome_text_all2.markdown(text)
    time.sleep(0.01)
time.sleep(0.2)

img.image("img/ai/ai_waits1.jpg", use_column_width=True)
welcome_text_all3 = left_container.empty()
text = ""
for word in welcome_text3.split():
    text += word + " "
    welcome_text_all3.markdown(text)
    time.sleep(0.01)
time.sleep(0.2)

welcome_text_all4 = left_container.empty()
text = ""
for word in welcome_text4.split():
    text += word + " "
    welcome_text_all4.markdown(text)
    time.sleep(0.01)
time.sleep(0.2)

img.image("img/ai/ai_welcomes.jpeg", use_column_width=True)
welcome_text_all5 = left_container.empty()
text = ""
for word in welcome_text5.split():
    text += word + " "
    welcome_text_all5.markdown(text)
    time.sleep(0.01)
time.sleep(0.2)
st.container()

########################################################################################################################
#-------------- COCKTAIL FINDER SECTION -------------------------------------------------------------------------------#
########################################################################################################################
#- containers
left_side, right_side = cocktail_finder.columns([2, 2])
left_container = left_side.container(border=True)

#- container's contents
text = "Ready for a taste adventure?"
left_container.subheader(text)

text = "Join me as your AI bartender and let's discover the ideal cocktails crafted just for you! ✨"
left_container.markdown(text)

img_cf = left_container.empty()
img_cf.image("img/ai/ai_welcomes_r.jpeg", use_column_width=True)

right_container = right_side.container(border=True)

cocktail_type = right_container.radio("Which drink journey would you like to embark on?", options=["Enjoy a spirited adventure with an :red[Alcoholic] Delight 🍸", "Savor the crisp taste of a :green[Non-alcoholic] Refresher 🍹"], index=0)

if cocktail_type == "Enjoy a spirited adventure with an :red[Alcoholic] Delight 🍸":
    st.toast(":red[Alcoholic] Delights are selected", icon='👍🏼')
    img_cf.image("img/ai/ai_cheers1_1_r.jpg", use_column_width=True)
    time.sleep(0.2)
    cocktail_df = cocktails_df[cocktails_df["alcoholic"] == "Alcoholic"]

elif cocktail_type == "Savor the crisp taste of a :green[Non-alcoholic] Refresher 🍹":
    st.toast(":green[Non-alcoholic] Refresher are selected", icon='👍🏼')
    img_cf.image("img/ai/ai_cheers1_2_r.jpg", use_column_width=True)
    time.sleep(0.2)
    cocktail_df = cocktails_df[cocktails_df["alcoholic"] == "Non alcoholic"]

#-- search settings
settings = left_side.container(border=True)
settings.markdown("Search Settings")
show_details = settings.toggle("Show me how to prepare as well")
shuffle_suggestions = settings.toggle("Shuffle Suggestions for each search", value=False)

########################################################################################################################
#-------------- DEFINE DATASET for ALCOHOLIC or NON-ALCOHOLIC DRINKS --------------------------------------------------#
########################################################################################################################
##- create cocktail names list
cocktail_names = sorted(list(set(cocktail for cocktail in cocktail_df["cocktail_name"])))
#-----------------------------------------------------------------------------------------------------------------------
##- create cocktail ingredients list
ing = "ingredients"
ing_list = sorted(list(set("".join(cocktail_df[ing]).split(","))))
ing_list = list(set([ing_.strip().lower() for ing_ in ing_list if not ing_.isspace()]))
##- apply corrections for cocktail ingredients list
ing_list = sorted(list(set([correct_words.get(ing, ing) for ing in ing_list])))
#-----------------------------------------------------------------------------------------------------------------------
##- create cocktail ingredients words list
ing_words_list = sorted(list(set(" ".join(ing_list).split())))
##- apply corrections for cocktail ingredients words list
ing_words_list = [correct_words.get(ing, ing) for ing in ing_words_list]
##- remove unrelated words from cocktail ingredients words list
ing_words_list = list(set([ing for ing in ing_words_list if ing not in remove_words and ing != "151"]))

##- final list for all ingredients
ingredients_all = sorted(list(set(ing_list + ing_words_list)))

right_container.divider()

#- search type options
right_options, left_options = right_container.columns(2)

#-- search type checkboxes
search_type = right_options.radio("Let's shake things up in a few ways:", options=["Pick a Cocktail Buddy!️", "Ingredients, Anyone?"], index=0)
right_container.divider()

if search_type == "Pick a Cocktail Buddy!️":
    st.toast("**Search for similar cocktails** is activated", icon='👍🏼')
    img_cf.image("img/ai/ai_waits2_r.jpg", use_column_width=True)
    time.sleep(0.2)

    text = "Pick a Cocktail Buddy!️"
    right_container.subheader(text)

    text = "Choose a delightful cocktail from the dropdown, and I'll unveil its kindred spirits, ready to party on your palate! 🍸💫🌌"
    right_container.markdown(text)

    selected_cocktail = right_container.selectbox(label="*Please select a Cocktail...*", options=cocktail_names, index=6)
    cocktail_similarity_level = right_container.select_slider("", options=["Low Similarity", "Partially Alike", "Closely Related"], value="Partially Alike")
    right_container.divider()

elif search_type == "Ingredients, Anyone?":
    st.toast("**Search with ingredients** is activated", icon='👍🏼')
    img_cf.image("img/ai/ai_waits1_r.jpg", use_column_width=True)
    time.sleep(0.2)

    text = "Ingredients, Anyone?"
    right_container.subheader(text)

    text = "Craving a specific taste? Choose your favorite ingredients, and I'll find cocktails that match your flavor wishes! 🍊🍋🍌🍍"
    right_container.markdown(text)

    ings_to_include = right_container.multiselect(label="*Please select some ingredients that your Cocktail should include...*", options=sorted(ing_list), default=None, placeholder="Choose some options")
    ings_to_exclude = right_container.multiselect(label="*Please select some ingredients that your Cocktail should :red[not] include...*", options=sorted(ingredients_all), default=None, placeholder="Choose some options")
    ingredients_similarity_level = right_container.select_slider("", options=["Low Level Intersection", "Harmonious Elements", "Synchronized Ingredients"], value="Harmonious Elements")
    right_container.divider()

#-- find cocktails button
list_button = right_container.button(":rainbow[Let's discover your next favorite Cocktail !]", use_container_width=True)
st.divider()

########################################################################################################################
#-------------- CALCULATE AND BRING SUGGESTIONS -----------------------------------------------------------------------#
########################################################################################################################
scaler = MinMaxScaler()

#- calculate results
if list_button:
    img_cf.image("img/ai/ai_cheers2_1_r.jpg", use_column_width=True)
    time.sleep(1)
    img_cf.image("img/ai/ai_cheers2_2_r.jpg", use_column_width=True)
    time.sleep(0.3)
    img_cf.image("img/ai/ai_cheers2_3_r.jpg", use_column_width=True)
    st.toast("Discovering delightful cocktails just for you.. 😎", icon='⬇')
    time.sleep(1)

    if search_type == "Pick a Cocktail Buddy!️":
        selected_cocktail_line = cocktail_df[cocktails_df["cocktail_name"] == str(selected_cocktail)]
        selected_cocktail_name = selected_cocktail_line.values[0][1]
        selected_cocktail_ing = selected_cocktail_line.values[0][3]
        selected_cocktail_dose = selected_cocktail_line.values[0][4]
        selected_cocktail_prep = selected_cocktail_line.values[0][5]
        selected_cocktail_img = selected_cocktail_line.values[0][6]

        if cocktail_similarity_level == "Closely Related":
            scoring_weight = "exact_match"
            thres1 = 0.5
            thres2 = 0.2
            thres3 = 0
        elif cocktail_similarity_level == "Partially Alike":
            scoring_weight = "arithmetical"
            thres1 = 0.5
            thres2 = 0.2
            thres3 = 0
        elif cocktail_similarity_level == "Low Similarity":
            scoring_weight = "arithmetical"
            thres1 = 0.5
            thres2 = 0.2
            thres3 = 0

        cocktail_df["similarity_scoring"] = cocktail_df["ingredients"].apply(lambda x: find_score(selected_cocktail_ing, x, scoring_weights=scoring_weight, report=False))
        suggestion_df_ordered = cocktail_df.sort_values("similarity_scoring", ascending=False)
        suggestion_df_ordered["similarity_scoring"] = scaler.fit_transform(suggestion_df_ordered["similarity_scoring"].values.reshape(-1, 1))
        suggestion_df_ordered = suggestion_df_ordered[~(suggestion_df_ordered["cocktail_name"] == selected_cocktail)]

        if cocktail_similarity_level == "Closely Related":
            suggestion_df_ordered = suggestion_df_ordered[(suggestion_df_ordered["similarity_scoring"] >= thres1) & (suggestion_df_ordered["similarity_scoring"] <= 1)]
            if shuffle_suggestions:
                len_df = len(suggestion_df_ordered)
                if len_df > 5:
                    suggestion_df_ordered = suggestion_df_ordered.sample(6)

        elif cocktail_similarity_level == "Partially Alike":
            suggestion_df_ordered = suggestion_df_ordered[(suggestion_df_ordered["similarity_scoring"] >= thres2) & (suggestion_df_ordered["similarity_scoring"] < thres1)]
            if shuffle_suggestions:
                len_df = len(suggestion_df_ordered)
                if len_df > 5:
                    suggestion_df_ordered = suggestion_df_ordered.sample(6)

        elif cocktail_similarity_level == "Low Similarity":
            suggestion_df_ordered = suggestion_df_ordered[(suggestion_df_ordered["similarity_scoring"] > thres3) & (suggestion_df_ordered["similarity_scoring"] < thres2)]
            if shuffle_suggestions:
                len_df = len(suggestion_df_ordered)
                if len_df > 5:
                    suggestion_df_ordered = suggestion_df_ordered.sample(6)

        len_df = len(suggestion_df_ordered)

        # suggestion 1
        if len_df >= 1:
            sugg1_name = suggestion_df_ordered.values[0][1]
            sugg1_ing = suggestion_df_ordered.values[0][3]
            sugg1_dose = suggestion_df_ordered.values[0][4]
            sugg1_prep = suggestion_df_ordered.values[0][5]
            sugg1_img = suggestion_df_ordered.values[0][6]
            sugg1_score = suggestion_df_ordered.values[0][13]

        # suggestion 2
        if len_df >= 2:
            sugg2_name = suggestion_df_ordered.values[1][1]
            sugg2_ing = suggestion_df_ordered.values[1][3]
            sugg2_dose = suggestion_df_ordered.values[1][4]
            sugg2_prep = suggestion_df_ordered.values[1][5]
            sugg2_img = suggestion_df_ordered.values[1][6]
            sugg2_score = suggestion_df_ordered.values[1][13]

        # suggestion 3
        if len_df >= 3:
            sugg3_name = suggestion_df_ordered.values[2][1]
            sugg3_ing = suggestion_df_ordered.values[2][3]
            sugg3_dose = suggestion_df_ordered.values[2][4]
            sugg3_prep = suggestion_df_ordered.values[2][5]
            sugg3_img = suggestion_df_ordered.values[2][6]
            sugg3_score = suggestion_df_ordered.values[2][13]

        # suggestion 4
        if len_df >= 4:
            sugg4_name = suggestion_df_ordered.values[3][1]
            sugg4_ing = suggestion_df_ordered.values[3][3]
            sugg4_dose = suggestion_df_ordered.values[3][4]
            sugg4_prep = suggestion_df_ordered.values[3][5]
            sugg4_img = suggestion_df_ordered.values[3][6]
            sugg4_score = suggestion_df_ordered.values[3][13]

        # suggestion 5
        if len_df >= 5:
            sugg5_name = suggestion_df_ordered.values[4][1]
            sugg5_ing = suggestion_df_ordered.values[4][3]
            sugg5_dose = suggestion_df_ordered.values[4][4]
            sugg5_prep = suggestion_df_ordered.values[4][5]
            sugg5_img = suggestion_df_ordered.values[4][6]
            sugg5_score = suggestion_df_ordered.values[4][13]

        # - suggestion tabs
        suggestions = cocktail_finder.container(border=True)
        selected_name_cocktail, sugg1_name_cocktail, sugg2_name_cocktail, sugg3_name_cocktail, sugg4_name_cocktail, sugg5_name_cocktail = suggestions.columns([1.5, 1, 1, 1, 1, 1])
        selected_cocktail, sugg1, sugg2, sugg3, sugg4, sugg5 = suggestions.columns([1.5, 1, 1, 1, 1, 1])

        if show_details:
            suggestions.divider()
            selected_cocktail_det, sugg1_det, sugg2_det, sugg3_det, sugg4_det, sugg5_det = suggestions.columns([1.5, 1, 1, 1, 1, 1])
            suggestions.divider()
            selected_cocktail_det2, sugg1_det2, sugg2_det2, sugg3_det2, sugg4_det2, sugg5_det2 = suggestions.columns([1.5, 1, 1, 1, 1, 1])

        html = "<div style='text-align:center; height: 0px;'>{}</div>".format(selected_cocktail_name)
        selected_name_cocktail.markdown(html, unsafe_allow_html=True)
        selected_cocktail.divider()
        selected_cocktail.image(selected_cocktail_img)
        selected_cocktail.markdown(selected_cocktail_ing.replace(",", "|").replace("|", ":gray[ | ]"))

        if show_details:
            selected_cocktail_det.markdown(":blue[*Proportions*]")
            selected_cocktail_det.markdown(":gray[*{}*]".format(selected_cocktail_dose.replace(",", "|").replace("|", ":gray[ | ]")))
            selected_cocktail_det2.markdown(":green[*Recipe*]")
            selected_cocktail_det2.markdown(":gray[*{}*]".format(selected_cocktail_prep.title().replace("\n", " ").strip().replace('"', "'").replace(".", "✔️")))

        if len_df == 0:
            if cocktail_similarity_level == "Closely Related":
                time.sleep(1)
                st.toast("Unfortunaly, no suggestion can be created...", icon='😔')
                sugg4.image("img/ai/ai_flying_empty_glass.jpg", use_column_width=True)
                sugg3.divider()
                sugg3.markdown("*No :gray['Closely Related'] matches this time! 😇*")
                sugg3.divider()
                time.sleep(3)
                sugg4.image("img/ai/ai_presents1.jpg", use_column_width=True)
                time.sleep(1)
                sugg3.markdown("*Shake things up a bit by tweaking the similarity options to :blue['Partially Alike'] or :blue['Low Similarity'] for a different perspective 😊*")
                sugg3.divider()

            elif cocktail_similarity_level == "Partially Alike":
                time.sleep(1)
                st.toast("Unfortunaly, no suggestion can be created...", icon='😔')
                sugg4.image("img/ai/ai_flying_empty_glass.jpg", use_column_width=True)
                sugg3.divider()
                sugg3.markdown("*No :gray['Closely Related'] matches this time! 😇*")
                sugg3.divider()
                time.sleep(3)
                sugg4.image("img/ai/ai_presents1.jpg", use_column_width=True)
                time.sleep(1)
                sugg3.markdown("*Shake things up a bit by tweaking the similarity options to :blue['Low Similarity'] for a different perspective 😊*")
                sugg3.divider()

        if len_df >= 1:
            html = "<div style='text-align:center'>{}</div>".format(sugg1_name)
            sugg1_name_cocktail.markdown(html, unsafe_allow_html=True)
            sugg1.divider()
            sugg1.image(load_img_and_resize(sugg1_img))
            sugg1.markdown(sugg1_ing.replace(",", "|").replace("|", ":gray[ | ]"))

            if show_details:
                sugg1_det.markdown("*:blue[Proportions]*")
                sugg1_det.markdown("*:gray[{}]*".format(sugg1_dose.replace(",", "|").replace("|", ":gray[ | ]")))
                sugg1_det2.markdown("*:green[Recipe]*")
                sugg1_det2.markdown("*:gray[{}]*".format(sugg1_prep.title().replace("\n", " ").strip().replace('"', "'").replace(".", "✔️")))

        if len_df >= 2:
            html = "<div style='text-align:center'>{}</div>".format(sugg2_name)
            sugg2_name_cocktail.markdown(html, unsafe_allow_html=True)
            sugg2.divider()
            sugg2.image(load_img_and_resize(sugg2_img))
            sugg2.markdown(sugg2_ing.replace(",", "|").replace("|", ":gray[ | ]"))

            if show_details:
                sugg2_det.markdown("*:blue[Proportions]*")
                sugg2_det.markdown("*:gray[{}]*".format(sugg2_dose.replace(",", "|").replace("|", ":gray[ | ]")))
                sugg2_det2.markdown("*:green[Recipe]*")
                sugg2_det2.markdown("*:gray[{}]*".format(sugg2_prep.title().replace("\n", " ").strip().replace('"', "'").replace(".", "✔️")))

        if len_df >= 3:
            html = "<div style='text-align:center'>{}</div>".format(sugg3_name)
            sugg3_name_cocktail.markdown(html, unsafe_allow_html=True)
            sugg3.divider()
            sugg3.image(load_img_and_resize(sugg3_img))
            sugg3.markdown(sugg3_ing.replace(",", "|").replace("|", ":gray[ | ]"))

            if show_details:
                sugg3_det.markdown("*:blue[Proportions]*")
                sugg3_det.markdown("*:gray[{}]*".format(sugg3_dose.replace(",", "|").replace("|", ":gray[ | ]")))
                sugg3_det2.markdown("*:green[Recipe]*")
                sugg3_det2.markdown("*:gray[{}]*".format(sugg3_prep.title().replace("\n", " ").strip().replace('"', "'").replace(".", "✔️")))

        if len_df >= 4:
            html = "<div style='text-align:center'>{}</div>".format(sugg4_name)
            sugg4_name_cocktail.markdown(html, unsafe_allow_html=True)
            sugg4.divider()
            sugg4.image(load_img_and_resize(sugg4_img))
            sugg4.markdown(sugg4_ing.replace(",", "|").replace("|", ":gray[ | ]"))

            if show_details:
                sugg4_det.markdown("*:blue[Proportions]*")
                sugg4_det.markdown("*:gray[{}]*".format(sugg4_dose.replace(",", "|").replace("|", ":gray[ | ]")))
                sugg4_det2.markdown("*:green[Recipe]*")
                sugg4_det2.markdown("*:gray[{}]*".format(sugg4_prep.title().replace("\n", " ").strip().replace('"', "'").replace(".", "✔️")))

        if len_df >= 5:
            html = "<div style='text-align:center'>{}</div>".format(sugg5_name)
            sugg5_name_cocktail.markdown(html, unsafe_allow_html=True)
            sugg5.divider()
            sugg5.image(load_img_and_resize(sugg5_img))
            sugg5.markdown(sugg5_ing.replace(",", "|").replace("|", ":gray[ | ]"))

            if show_details:
                sugg5_det.markdown("*:blue[Proportions]*")
                sugg5_det.markdown("*:gray[{}]*".format(sugg5_dose.replace(",", "|").replace("|", ":gray[ | ]")))
                sugg5_det2.markdown("*:green[Recipe]*")
                sugg5_det2.markdown("*:gray[{}]*".format(sugg5_prep.title().replace("\n", " ").strip().replace('"', "'").replace(".", "✔️")))

        if not len_df <= 1:
            st.toast("Suggestions have been created", icon='👌🏼')
            st.toast("Cheerrs !!", icon='🥂')

    elif search_type == "Ingredients, Anyone?":

        if ingredients_similarity_level == "Synchronized Ingredients":
            scoring_weight = "exact_match"
            thres1 = 0.8
            thres2 = 0.3
            thres3 = 0
        elif ingredients_similarity_level == "Harmonious Elements":
            scoring_weight = "arithmetical"
            thres1 = 0.8
            thres2 = 0.3
            thres3 = 0
        elif ingredients_similarity_level == "Low Level Intersection":
            scoring_weight = "arithmetical"
            thres1 = 0.8
            thres2 = 0.3
            thres3 = 0

        cocktail_df["similarity_scoring"] = cocktail_df["ingredients"].apply(lambda x: find_score(", ".join(ings_to_include), x, scoring_weights=scoring_weight, report=False))
        cocktail_df["exclude_scoring"] = cocktail_df["ingredients"].apply(lambda x: find_score(", ".join(ings_to_exclude), x, scoring_weights="equally", report=False))
        cocktail_df["final_scoring"] = np.where(cocktail_df["exclude_scoring"] > 0, 0, cocktail_df["similarity_scoring"])
        suggestion_df_ordered = cocktail_df.sort_values(["final_scoring", "exclude_scoring"], ascending=[False, True])
        suggestion_df_ordered["final_scoring"] = scaler.fit_transform(suggestion_df_ordered["final_scoring"].values.reshape(-1, 1))

        if ingredients_similarity_level == "Synchronized Ingredients":
            suggestion_df_ordered = suggestion_df_ordered[(suggestion_df_ordered["final_scoring"] >= thres1)]
            if shuffle_suggestions:
                len_df = len(suggestion_df_ordered)
                if len_df > 5:
                    suggestion_df_ordered = suggestion_df_ordered.sample(6)

        elif ingredients_similarity_level == "Harmonious Elements":
            suggestion_df_ordered = suggestion_df_ordered[(suggestion_df_ordered["final_scoring"] >= thres2)]
            if shuffle_suggestions:
                len_df = len(suggestion_df_ordered)
                if len_df > 5:
                    suggestion_df_ordered = suggestion_df_ordered.sample(6)

        elif ingredients_similarity_level == "Low Level Intersection":
            suggestion_df_ordered = suggestion_df_ordered[(suggestion_df_ordered["final_scoring"] > thres3)]
            if shuffle_suggestions:
                len_df = len(suggestion_df_ordered)
                if len_df > 5:
                    suggestion_df_ordered = suggestion_df_ordered.sample(6)

        len_df = len(suggestion_df_ordered)

        # suggestion 1
        if len_df >= 1:
            sugg1_name = suggestion_df_ordered.values[0][1]
            sugg1_ing = suggestion_df_ordered.values[0][3]
            sugg1_dose = suggestion_df_ordered.values[0][4]
            sugg1_prep = suggestion_df_ordered.values[0][5]
            sugg1_img = suggestion_df_ordered.values[0][6]
            sugg1_score = suggestion_df_ordered.values[0][15]

        # suggestion 2
        if len_df >= 2:
            sugg2_name = suggestion_df_ordered.values[1][1]
            sugg2_ing = suggestion_df_ordered.values[1][3]
            sugg2_dose = suggestion_df_ordered.values[1][4]
            sugg2_prep = suggestion_df_ordered.values[1][5]
            sugg2_img = suggestion_df_ordered.values[1][6]
            sugg2_score = suggestion_df_ordered.values[1][15]

        # suggestion 3
        if len_df >= 3:
            sugg3_name = suggestion_df_ordered.values[2][1]
            sugg3_ing = suggestion_df_ordered.values[2][3]
            sugg3_dose = suggestion_df_ordered.values[2][4]
            sugg3_prep = suggestion_df_ordered.values[2][5]
            sugg3_img = suggestion_df_ordered.values[2][6]
            sugg3_score = suggestion_df_ordered.values[2][15]

        # suggestion 4
        if len_df >= 4:
            sugg4_name = suggestion_df_ordered.values[3][1]
            sugg4_ing = suggestion_df_ordered.values[3][3]
            sugg4_dose = suggestion_df_ordered.values[3][4]
            sugg4_prep = suggestion_df_ordered.values[3][5]
            sugg4_img = suggestion_df_ordered.values[3][6]
            sugg4_score = suggestion_df_ordered.values[3][15]

        # suggestion 5
        if len_df >= 5:
            sugg5_name = suggestion_df_ordered.values[4][1]
            sugg5_ing = suggestion_df_ordered.values[4][3]
            sugg5_dose = suggestion_df_ordered.values[4][4]
            sugg5_prep = suggestion_df_ordered.values[4][5]
            sugg5_img = suggestion_df_ordered.values[4][6]
            sugg5_score = suggestion_df_ordered.values[4][15]

        # - suggestion tabs
        suggestions = cocktail_finder.container(border=True)
        selected_name_cocktail, sugg1_name_cocktail, sugg2_name_cocktail, sugg3_name_cocktail, sugg4_name_cocktail, sugg5_name_cocktail = suggestions.columns([1.5, 1, 1, 1, 1, 1])
        selected_cocktail, sugg1, sugg2, sugg3, sugg4, sugg5 = suggestions.columns([1.5, 1, 1, 1, 1, 1])

        if show_details:
            suggestions.divider()
            selected_cocktail_det, sugg1_det, sugg2_det, sugg3_det, sugg4_det, sugg5_det = suggestions.columns([1.5, 1, 1, 1, 1, 1])
            suggestions.divider()
            selected_cocktail_det2, sugg1_det2, sugg2_det2, sugg3_det2, sugg4_det2, sugg5_det2 = suggestions.columns([1.5, 1, 1, 1, 1, 1])

        html = "<div style='text-align:center; height: 0px;'>{}</div>".format("📜   Your Personal Elixir   📜")
        selected_name_cocktail.markdown(html, unsafe_allow_html=True)
        selected_cocktail.divider()

        if len(ings_to_include) > 0 or len(ings_to_exclude) > 0:
            selected_cocktail.image("img/empty_glass_shaker.jpg")
            if len(ings_to_include) > 0 and len(ings_to_exclude) == 0:
                selected_cocktail.markdown("*Sculpting your flavor profile with :green[{}].*".format(", ".join(ings_to_include)))
            elif len(ings_to_include) == 0 and len(ings_to_exclude) > 0:
                selected_cocktail.markdown("*I am stay out of the mix the ingredients :red[{}].*".format(", ".join(ings_to_exclude)))
            else:
                selected_cocktail.markdown("*Sculpting your flavor profile with :green[{}] by ensuring that :red[{}] stay out of the mix.*".format(", ".join(ings_to_include), ", ".join(ings_to_exclude)))
        else:
            selected_cocktail.markdown("*Waiting for your handcrafted selections...*")

        if len_df == 0:
            if ingredients_similarity_level == "Synchronized Ingredients":
                time.sleep(1)
                st.toast("Unfortunaly, no suggestion can be created...", icon='😔')
                sugg4.image("img/ai/ai_flying_empty_glass.jpg", use_column_width=True)
                sugg3.divider()
                sugg3.markdown("*No :gray['Synchronized Ingredients'] matches this time! 😇*")
                sugg3.divider()
                time.sleep(3)
                sugg4.image("img/ai/ai_presents1.jpg", use_column_width=True)
                time.sleep(1)
                sugg3.markdown("*Shake things up a bit by tweaking the similarity options to :blue['Harmonious Elements'] or :blue['Low Level Intersection'] for a different perspective 😊*")
                sugg3.divider()

            elif ingredients_similarity_level == "Harmonious Elements":
                time.sleep(1)
                st.toast("Unfortunaly, no suggestion can be created...", icon='😔')
                sugg4.image("img/ai/ai_flying_empty_glass.jpg", use_column_width=True)
                sugg3.divider()
                sugg3.markdown("*No :gray['Closely Related'] matches this time! 😇*")
                sugg3.divider()
                time.sleep(3)
                sugg4.image("img/ai/ai_presents1.jpg", use_column_width=True)
                time.sleep(1)
                sugg3.markdown("*Shake things up a bit by tweaking the similarity options to :blue['Low Level Intersection'] for a different perspective 😊*")
                sugg3.divider()

        if len_df >= 1:
            html = "<div style='text-align:center'>{}</div>".format(sugg1_name)
            sugg1_name_cocktail.markdown(html, unsafe_allow_html=True)
            sugg1.divider()
            sugg1.image(load_img_and_resize(sugg1_img))
            sugg1.markdown(sugg1_ing.replace(",", "|").replace("|", ":gray[ | ]"))

            if show_details:
                sugg1_det.markdown("*:blue[Proportions]*")
                sugg1_det.markdown("*:gray[{}]*".format(sugg1_dose.replace(",", "|").replace("|", ":gray[ | ]")))
                sugg1_det2.markdown("*:green[Recipe]*")
                sugg1_det2.markdown("*:gray[{}]*".format(sugg1_prep.title().replace("\n", " ").strip().replace('"', "'").replace(".", "✔️")))

        if len_df >= 2:
            html = "<div style='text-align:center'>{}</div>".format(sugg2_name)
            sugg2_name_cocktail.markdown(html, unsafe_allow_html=True)
            sugg2.divider()
            sugg2.image(load_img_and_resize(sugg2_img))
            sugg2.markdown(sugg2_ing.replace(",", "|").replace("|", ":gray[ | ]"))

            if show_details:
                sugg2_det.markdown("*:blue[Proportions]*")
                sugg2_det.markdown("*:gray[{}]*".format(sugg2_dose.replace(",", "|").replace("|", ":gray[ | ]")))
                sugg2_det2.markdown("*:green[Recipe]*")
                sugg2_det2.markdown("*:gray[{}]*".format(sugg2_prep.title().replace("\n", " ").strip().replace('"', "'").replace(".", "✔️")))

        if len_df >= 3:
            html = "<div style='text-align:center'>{}</div>".format(sugg3_name)
            sugg3_name_cocktail.markdown(html, unsafe_allow_html=True)
            sugg3.divider()
            sugg3.image(load_img_and_resize(sugg3_img))
            sugg3.markdown(sugg3_ing.replace(",", "|").replace("|", ":gray[ | ]"))

            if show_details:
                sugg3_det.markdown("*:blue[Proportions]*")
                sugg3_det.markdown("*:gray[{}]*".format(sugg3_dose.replace(",", "|").replace("|", ":gray[ | ]")))
                sugg3_det2.markdown("*:green[Recipe]*")
                sugg3_det2.markdown("*:gray[{}]*".format(sugg3_prep.title().replace("\n", " ").strip().replace('"', "'").replace(".", "✔️")))

        if len_df >= 4:
            html = "<div style='text-align:center'>{}</div>".format(sugg4_name)
            sugg4_name_cocktail.markdown(html, unsafe_allow_html=True)
            sugg4.divider()
            sugg4.image(load_img_and_resize(sugg4_img))
            sugg4.markdown(sugg4_ing.replace(",", "|").replace("|", ":gray[ | ]"))

            if show_details:
                sugg4_det.markdown("*:blue[Proportions]*")
                sugg4_det.markdown("*:gray[{}]*".format(sugg4_dose.replace(",", "|").replace("|", ":gray[ | ]")))
                sugg4_det2.markdown("*:green[Recipe]*")
                sugg4_det2.markdown("*:gray[{}]*".format(sugg4_prep.title().replace("\n", " ").strip().replace('"', "'").replace(".", "✔️")))

        if len_df >= 5:
            html = "<div style='text-align:center'>{}</div>".format(sugg5_name)
            sugg5_name_cocktail.markdown(html, unsafe_allow_html=True)
            sugg5.divider()
            sugg5.image(load_img_and_resize(sugg5_img))
            sugg5.markdown(sugg5_ing.replace(",", "|").replace("|", ":gray[ | ]"))

            if show_details:
                sugg5_det.markdown("*:blue[Proportions]*")
                sugg5_det.markdown("*:gray[{}]*".format(sugg5_dose.replace(",", "|").replace("|", ":gray[ | ]")))
                sugg5_det2.markdown("*:green[Recipe]*")
                sugg5_det2.markdown("*:gray[{}]*".format(sugg5_prep.title().replace("\n", " ").strip().replace('"', "'").replace(".", "✔️")))

        if not len_df == 0:
            st.toast("Suggestions have been created", icon='👌🏼')
            st.toast("Cheerrs !!", icon='🥂')

########################################################################################################################
#-------------- MEASUREMENTS SECTION ----------------------------------------------------------------------------------#
########################################################################################################################
left_m, right_m, right_me = measurement.columns([2, 1, 2])
m_info1 = left_m.container(border=True)
m_converter = right_m.container(border=True)
m_info2 = right_me.container(border=True)
rainbow_text = """
<div style='text-align:center; color:white; font-size:20px;'>
  <span style='background-image: linear-gradient(to right, violet, indigo, blue, green, yellow, orange, red); -webkit-background-clip: text; color: transparent;'>
    Measurement Converter
  </span>
</div>
"""
m_converter.markdown(rainbow_text, unsafe_allow_html=True)
m_converter.divider()

#- welcome section
m_info1.subheader("  🌈 Decoding Cocktail Measurements 🍹   ")
m_info1.divider()
m_info1.markdown(""":green[🥃 Ounce (oz):] *Used for measuring alcoholic ingredients like spirits in cocktails, it's roughly equivalent to a shot (approximately 30 ml).*""")
m_info1.markdown(""":green[🍶 Centiliter (cl):] *A metric unit smaller than an ounce, used for precise measurements in cocktails (1 cl is approximately 0.34 oz).*""")
m_info1.markdown(""":green[🥛 Milliliter (ml):] *An even smaller metric unit than an ounce, commonly used for very precise measurements in cocktails (1 ml is approximately 0.03 oz).*""")
m_info1.markdown(""":green[🥄 Tablespoon (tblsp):] *An abbreviation for a larger liquid measurement, used for adding ingredients like syrups or juices in cocktails (approximately 15 ml, about half an ounce).*""")
m_info1.markdown(""":green[🍵 Teaspoon (tsp):] *An abbreviation for a smaller liquid measurement, used for ingredients like bitters or extracts in cocktails (approximately 5 ml, about one-sixth of an ounce).*""")
m_info1.markdown(""":green[🥃 Shot:] *A standard unit of volume in cocktails, typically around 1.5 fluid ounces (44 ml). When a recipe calls for a 'shot,' it signifies the use of this standard measure, ensuring consistency in the drink's strength and flavor.*""")
m_info1.markdown(""":green[🍵 Cup:] *A larger liquid measurement, typically used for mixers or larger quantities of ingredients in cocktails (1 cup is approximately 8 ounces or 240 milliliters).*""")
m_info2.subheader("  🔍 Exploring Cocktail Metrics 🍸  ")
m_info2.divider()
m_info2.markdown(""":blue[🍋 1 Twist of:] *The peel of a citrus fruit twisted over the cocktail to release its aromatic oils. Adds a burst of citrus essence to the drink.*""")
m_info2.markdown(""":blue[🔪 1/2 Slice:] *Half of a thin portion of fruit, often used as a garnish or muddled in the cocktail for flavor.*""")
m_info2.markdown(""":blue[⚖️ Part:] *A versatile unit used to express ratios in a cocktail recipe. For example, 1 part can be any consistent measurement, and the other parts are adjusted accordingly.*""")
m_info2.markdown(""":blue[💧 Dash:] *A small and quick pour, often used for ingredients like bitters. It adds a subtle but essential flavor element to the cocktail.*""")
m_info2.markdown(""":blue[💦 Splash:] *Similar to a dash, a quick and small pour of a liquid ingredient. It imparts a hint of flavor without dominating the overall taste.*""")
m_info2.markdown(""":blue[🍍 Chunk:] *A single, bite-sized piece of an ingredient, such as fruit or ice. Adds texture and flavor to the cocktail.*""")
m_info2.markdown(""":blue[🍺 Pint:] *A larger volume measurement, often used for mixing larger batches of cocktails (1 pint is approximately 16 ounces or 473 milliliters).*""")
m_info2.markdown(""":blue[🍶 Quart:] *An even larger volume measurement, used for larger quantities in some cocktail recipes (1 quart is approximately 32 ounces or 946 milliliters).*""")

#- converter section
convert_left, convert_right = m_converter.columns([1, 2])
convert_left.markdown("<div style='text-align:right; height:60px; padding:4px'>Amount</div>", unsafe_allow_html=True)
convert_left.markdown("<div style='text-align:right; height:60px; padding:4px'>From</div>", unsafe_allow_html=True)
convert_left.markdown("<div style='text-align:right; height:60px; padding:4px'>To</div>", unsafe_allow_html=True)
from_amount = convert_right.selectbox(label="", options=range(1,200), label_visibility="collapsed")
calculator_from = convert_right.selectbox(label="", options=lst.measurement_types, label_visibility="collapsed", key="0")
calculator_to = convert_right.selectbox(label="", options=lst.measurement_types, label_visibility="collapsed", key="1")
converted_amount = measurements_converter(calculator_from, calculator_to, from_amount)
if isinstance(converted_amount, float) and converted_amount.is_integer():
    converted_amount = int(converted_amount)
else:
    converted_amount = round(converted_amount,2)
m_converter.divider()
result_text = "<div style='display: flex; justify-content: center; font-family: cursive, sans-serif; font-size:18px'>  {}   {}  🔄  {}   {}  </div>".format(from_amount, calculator_from, converted_amount, calculator_to)
m_converter.write(result_text, unsafe_allow_html=True)
m_converter.divider()
m_converter.image("img/measurements.jpg")

