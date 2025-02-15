import streamlit as st
import requests
from PIL import Image
import io
import os

# ---- APP CONFIGURATION ----
st.set_page_config(page_title="Kitchen Copilot", page_icon="images/KitchenCopilot_Logo.png", layout="wide")

# ---- FORCE LIGHT THEME (REMOVE BLACK ELEMENTS) ----
st.markdown("""
    <style>
        /* Ensure all text is black */
        * {
            color: #000000 !important;
        }
        /* Full-width Orange Title Bar */
        .title-bar {
            background-color: #FF6F3C;
            padding: 20px;
            color: white;
            text-align: center;
            font-size: 22px;
            font-weight: bold;
            width: 100%;
        }
        /* Ensure input fields, select boxes, file uploader, and buttons are white with black text */
        input[type="text"], select, .stTextInput>div>div>input, .stSelectbox>div>div>select, 
        .stFileUploader>div>div>button, .stButton>button {
            background-color: #FFFFFF !important;
            color: #000000 !important;  /* Ensure text is black */
            border: 1px solid #CCC !important;
            border-radius: 8px;
            padding: 12px;
            width: 100%;
        }
        /* Ensure the file uploader box is white */
        .stFileUploader>div {
            background-color: #FFFFFF !important;
            border: 1px solid #CCC !important;
            color: #000000 !important;
            border-radius: 8px;
        }
        /* Ensure "Dietary Preferences" and "All Recipes" select boxes are white */
        .stSelectbox>div>div {
            background-color: #FFFFFF !important;
        }
        /* Ensure "All Recipes" text is black */
        .stSelectbox>div>div>select option {
            color: #000000 !important;
        }
        /* White background for entire app */
        html, body, [data-testid="stAppViewContainer"] {
            background-color: #FAF9F6 !important;
            color: #333 !important;
        }
        /* Full-width Orange Title Bar */
        .title-bar {
            background-color: #FF6F3C;
            padding: 20px;
            color: white;
            text-align: center;
            font-size: 22px;
            font-weight: bold;
            width: 100%;
        }
        /* Ensure text fields and dropdowns are white */
        input[type="text"], select, .stTextInput>div>div>input, .stSelectbox>div>div>select, .stFileUploader>div>div>button {
            background-color: #FFFFFF !important;
            color: #333 !important;
            border: 1px solid #CCC !important;
            border-radius: 8px;
            padding: 12px;
            width: 100%;
        }
        /* Style buttons */
        .stButton>button {
            background-color: #FF6F3C !important;
            color: white !important;
            font-size: 16px;
            font-weight: bold;
            border-radius: 10px;
            padding: 12px;
            width: 100%;
        }
        /* Styled container to simulate input field */
        .input-container {
            background: white;
            border-radius: 10px;
            padding: 10px;
            border: 1px solid #CCC;
            width: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
            font-weight: bold;
            color: #666;
        }
        /* Ingredient and Recipe Cards */
        .ingredient-card, .recipe-card {
            background: white;
            border-radius: 12px;
            padding: 12px;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
            text-align: center;
            font-size: 14px;
            margin-bottom: 15px;
        }
    </style>
""", unsafe_allow_html=True)

# ---- HEADER ----
st.markdown("""
    <style>
        /* Full-width Orange Header */
        .header-bar {
            background-color: #FF6F3C;
            padding: 15px 20px;
            color: white !important;
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-size: 20px;
            font-weight: bold;
            width: 100%;
            border-bottom-left-radius: 15px;
            border-bottom-right-radius: 15px;
        }
        /* Left-aligned title */
        .header-title {
            margin: 0;
            font-size: 18px;
            font-weight: normal;
            color: white !important;  /* Ensure title text remains white */
        }
        /* Right-aligned icons */
        .header-icons {
            display: flex;
            gap: 15px;
            align-items: center;
        }
        .header-icons img {
            width: 22px; /* Adjust icon size */
            height: 22px;
            filter: invert(1);
        }
    </style>
    <div class="header-bar">
        <span class="header-title">Explore Recipes</span>
        <div class="header-icons">
            <img src="https://cdn-icons-png.flaticon.com/512/134/134819.png" alt="Chat Icon">
            <img src="https://cdn-icons-png.flaticon.com/512/3602/3602145.png" alt="Bell Icon">  <!-- Updated Bell Icon -->
            <img src="https://cdn-icons-png.flaticon.com/512/5662/5662990.png" alt="Menu Icon">
        </div>
    </div>
""", unsafe_allow_html=True)


# ---- IMAGE UPLOAD & PROCESSING SECTION ----
st.markdown("<div class='input-container'>📤 Upload Your Leftover Food</div>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"])

if uploaded_file:
    col1, col2 = st.columns([1, 2])

    with col1:
        image = Image.open(uploaded_file)
        st.image(image, caption="📷 Uploaded Image", use_column_width=True)

    # Convert image to bytes
    img_bytes = io.BytesIO()
    image.save(img_bytes, format="JPEG")
    img_bytes.seek(0)  # Reset stream position
    print("✅ Image uploaded successfully")

    if st.button("🔍 Identify Ingredients"):
        with st.spinner("Processing..."):
            try:
                # Log request details
                print("🚀 Sending request to API...")
                print(f"Image Size: {len(img_bytes.getvalue())} bytes")

                # Send image to backend API
                response = requests.post(
                    "http://127.0.0.1:5000/GPT/send-image",
                    files={"file": ("image.jpg", img_bytes, "image/jpeg")}
                )

                # Debug response
                print(f"📡 Response Status Code: {response.status_code}")
                print(f"📡 Response Text: {response.text}")

                if response.status_code == 200:
                    data = response.json()
                    st.session_state["ingredients"] = data.get("ingredients", [])
                    st.session_state["recipes"] = data.get("recipes", [])

                    if not st.session_state["ingredients"]:
                        st.warning("⚠️ No ingredients detected. Try a different image.")
                    else:
                        st.success("✅ Ingredients Identified!")
                else:
                    st.error(f"🚨 Error: {response.json().get('error', 'Unknown error')}")
                    print(f"❌ API Error: {response.json()}")

            except requests.exceptions.RequestException as req_err:
                st.error(f"🔴 Request Exception: {str(req_err)}")
                print(f"🔴 Request Exception: {req_err}")

            except Exception as e:
                st.error(f"❌ Failed to process image: {str(e)}")
                print(f"❌ General Error: {e}")


# ---- DISPLAY INGREDIENT LIST ONLY AFTER IDENTIFICATION ----
if "ingredients" in st.session_state and st.session_state["ingredients"]:
    st.markdown("<div class='input-container'>📝 Identified Ingredients</div>", unsafe_allow_html=True)

    if "editable_ingredients" not in st.session_state:
        st.session_state["editable_ingredients"] = list(st.session_state["ingredients"])

    edited_ingredients = []
    
    for i, ingredient in enumerate(st.session_state["editable_ingredients"]):
        col1, col2, col3 = st.columns([2, 1, 1])  # Create columns for layout

        with col1:
            new_value = st.text_input("", ingredient, key=f"ingredient_{i}", label_visibility="collapsed")
            edited_ingredients.append(new_value)

        with col2:
            st.image(f"https://www.themealdb.com/images/ingredients/{new_value}.png", width=80)

        with col3:
            if st.button("✏️", key=f"edit_{i}"):  # Edit button
                st.session_state["editable_ingredients"][i] = new_value
                st.rerun()

            if st.button("❌", key=f"delete_{i}"):  # Delete button
                st.session_state["editable_ingredients"].remove(ingredient)
                st.rerun()

    # ---- ADD NEW INGREDIENT FUNCTIONALITY ----
    new_ingredient = st.text_input("➕ Add a New Ingredient", placeholder="Enter ingredient name", label_visibility="collapsed")

    if st.button("Add Ingredient", key="add_ingredient"):
        if new_ingredient and new_ingredient not in st.session_state["editable_ingredients"]:
            st.session_state["editable_ingredients"].append(new_ingredient)
            st.rerun()

# ---- GENERATE RECIPES (AUTO-FINALIZES INGREDIENTS) ----
if "editable_ingredients" in st.session_state and len(st.session_state["editable_ingredients"]) > 0:
    # ---- USER PREFERENCES ----
    st.markdown("<div class='input-container'>🎯 Customize Your Recipe</div>", unsafe_allow_html=True)

    dietary_pref = st.selectbox(
        "Dietary Preferences", 
        ["🎯 Dietary Preferences", "None", "Vegetarian", "Vegan", "Gluten-Free", "Keto"], 
        index=0, 
        label_visibility="collapsed"
    )

    seasoning_pref = st.selectbox(
        "Seasoning Preference",
        ["🌶️ Spice Level", "Mild", "Medium", "Spicy", "No Preference"],
        index=0,
        label_visibility="collapsed"
    )

    cooking_time_pref = st.selectbox(
        "Cooking Time",
        ["⏳ Cooking Time", "Quick (Under 30 min)", "Moderate (30-60 min)", "Slow Cooked (1hr+)", "No Preference"],
        index=0,
        label_visibility="collapsed"
    )

    recipe_style_pref = st.selectbox(
        "Recipe Style",
        ["🍽️ Recipe Style", "Classic", "Vegan", "Spicy", "Mediterranean", "Asian Fusion", "No Preference"],
        index=0,
        label_visibility="collapsed"
    )

    user_preferences = {
        "Dietary Preference": dietary_pref if dietary_pref != "🎯 Dietary Preferences" else None,
        "Seasoning Preference": seasoning_pref if seasoning_pref != "🌶️ Spice Level" else None,
        "Cooking Time": cooking_time_pref if cooking_time_pref != "⏳ Cooking Time" else None,
        "Recipe Style": recipe_style_pref if recipe_style_pref != "🍽️ Recipe Style" else None
    }

    user_preferences = {k: v for k, v in user_preferences.items() if v}

    # Display Debugging Information (JSON Format)
    st.markdown("### 🛠 Debugging Information")
    st.json({
        "Final Ingredients": st.session_state["editable_ingredients"],
        "User Preferences": user_preferences
    })

    # Final Generate Recipes button
    if st.button("🍽️ Generate Recipes", key="generate_recipes"):
        st.session_state["final_ingredients"] = st.session_state["editable_ingredients"]

        with st.spinner("Creating delicious recipes..."):
            recipes = [
                {"name": "Tomato Cheese Salad", "ingredients": ["Tomato", "Cheese"], "instructions": "Mix everything and serve."},
                {"name": "Grilled Cheese Sandwich", "ingredients": ["Cheese", "Bread"], "instructions": "Grill with butter and serve."}
            ]
            st.markdown("<div class='input-container'>🍛 Suggested Recipes</div>", unsafe_allow_html=True)
            for recipe in recipes:
                st.markdown(f"### {recipe['name']}")
                st.write(f"**Ingredients:** {', '.join(recipe['ingredients'])}")
                st.write(f"**Instructions:** {recipe['instructions']}")


# ---- SEARCH & FILTER SECTION ----
search_query = st.text_input("Search", placeholder="🔍 Search Recipe", label_visibility="collapsed")

col1, col2 = st.columns([3, 1])
with col1:
    st.selectbox("", ["All Recipes", "Vegetarian", "Quick Meals", "Desserts"], key="cookbook_select")
with col2:
    st.button("+ Add New", key="add_new")

# ---- MOCK RECIPE DATA ----
image_folder = "images"

recipes = [
    {"name": "Applesauce Cake", "time": "45 minutes", "image": os.path.join(image_folder, "AppleSauceCake.jpg")},
    {"name": "Lemon, Garlic and Thyme Roast Chicken", "time": "45 minutes", "image": os.path.join(image_folder, "RoastChicken.jpeg")},
    {"name": "Quick and Easy Caprese Salad", "time": "45 minutes", "image": os.path.join(image_folder, "CapreseSalad.jpeg")},
    {"name": "Quinoa Tabouli with Lemon Garlic Shrimp", "time": "45 minutes", "image": os.path.join(image_folder, "GarlicShrimp.jpeg")},
    {"name": "Falafels With Tahini Sauce", "time": "45 minutes", "image": os.path.join(image_folder, "Falafels.jpg")},
    {"name": "Eggless Brownies", "time": "45 minutes", "image": os.path.join(image_folder, "Brownie.jpeg")},
]

# ---- RECIPE CATEGORIES ----
st.markdown("<div class='input-container'>🍔 American Recipes</div>", unsafe_allow_html=True)
cols = st.columns(3)
for i, recipe in enumerate(recipes[:3]):
    with cols[i]:
        st.image(recipe["image"], width=30, use_column_width=True)
        st.markdown(f"**{recipe['name']}**")
        st.markdown(f"⏳ {recipe['time']}")

st.markdown("<div class='input-container'>🍕 European Recipes</div>", unsafe_allow_html=True)
cols = st.columns(3)
for i, recipe in enumerate(recipes[3:]):
    with cols[i]:
        st.image(recipe["image"], width=30, use_column_width=True)
        st.markdown(f"**{recipe['name']}**")
        st.markdown(f"⏳ {recipe['time']}")