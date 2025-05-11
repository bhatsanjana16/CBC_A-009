import json

def load_schemes(json_path="data/schemes.json"):
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading schemes: {e}")
        return {}

def get_applicable_schemes(occupation=None, state=None):
    schemes = load_schemes()
    matched = []

    for name, details in schemes.items():
        eligible_occupations = [o.lower() for o in details["eligibility"].get("occupation", [])]
        eligible_states = [s.lower() for s in details["eligibility"].get("state", [])]

        occ_match = not occupation or occupation.lower() in eligible_occupations
        state_match = not state or state.lower() in eligible_states

        if occ_match and state_match:
            matched.append({
                "name": name,
                "description": details["description"],
                "registration_link": details["registration_link"]
            })

    return matched
