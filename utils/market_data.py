import pandas as pd

df = pd.read_csv("data/market_prices.csv")

def get_market_price(product, location=None):
    filtered = df[df['product'].str.contains(product, case=False, na=False)]
    if location:
        filtered = filtered[filtered['location'].str.contains(location, case=False, na=False)]
    if not filtered.empty:
        price = filtered.iloc[0]['price']
        return f"The price of {product} in {location or 'your area'} is {price}."
    return f"Price for {product} not found."

# import pandas as pd

# market_df = pd.read_csv("data/market_prices.csv")
# print("Loaded Data:\n", market_df.head())
# schemes_df = pd.read_csv("data/govt_schemes.csv")

# def get_market_price(commodity, location=None):
#     filtered = market_df[market_df['Commodity'].str.contains(commodity, case=False, na=False)]
#     if location:
#         filtered = filtered[filtered['State'].str.contains(location, case=False, na=False)]
    
#     if not filtered.empty:
#         row = filtered.iloc[0]
#         return f"The modal price of {commodity} in {row['Market']}, {row['District']}, {row['State']} is {row['Modal Price']}."
#     return "Sorry, I couldn't find market price information for that query."

# def get_applicable_schemes(category=None, state=None):
#     filtered = schemes_df.copy()

#     if category:
#         filtered = filtered[filtered['Target Beneficiaries'].str.contains(category, case=False, na=False)]
#     if state:
#         filtered = filtered[filtered['State'].str.contains(state, case=False, na=False)]

#     if filtered.empty:
#         return "No applicable schemes found."

#     # Return first 2 results as sample response
#     responses = []
#     for _, row in filtered.head(2).iterrows():
#         resp = f"Scheme: {row['Scheme Name']}\nEligibility: {row['Eligibility']}\nApply here: {row['Application Link']}"
#         responses.append(resp)

#     return "\n\n".join(responses)

# import os
# import pandas as pd

# # Load CSV using an absolute path
# DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "market_prices.csv")
# df = pd.read_csv(DATA_PATH)

# def get_market_price(product, location=None):
#     print(f"Searching for product: {product}, location: {location}")

#     # Try to match product in the 'Commodity' column
#     filtered = df[df['Commodity'].str.contains(product, case=False, na=False)]

#     if location:
#         # Match location in 'State' or 'District'
#         filtered = filtered[
#             filtered['State'].str.contains(location, case=False, na=False) |
#             filtered['District'].str.contains(location, case=False, na=False)
#         ]

#     if not filtered.empty:
#         price = filtered.iloc[0]['Modal Price']
#         return f"The modal price of {product} in {location or 'your area'} is {price}."
    
#     return f"Price for {product} not found."
# print(df.columns)



