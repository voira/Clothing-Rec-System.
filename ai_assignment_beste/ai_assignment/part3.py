from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load the dataset (Ensure 'image_url' column exists)
df = pd.read_csv("C:/Users/beste/Downloads/ai_assignment/sampled_data.csv")

# Define scoring function based on body type
def score_clothing(item, body_type):
    score = 0
    if body_type == 'apple':
        if item["tops_fit"] in ["regular-fit-tops", 'oversized-tops']: 
            score += 2
        if item["neckline_type"] in ["v-neck", "sweetheart-neck", "round-v-neck", "shoulder-off"]:  
            score += 2
        if item["tops_length"] in ["thigh-length", "long"]:  
            score += 2
        if item["style"] in ["casuals", "feminine"]:
            score += 2
        if item["sleeve_type"] == "flare-sleeve":
            score += 2
        if item["waist_type"] == "mid-waist":
            score += 2   
        if item["bottoms_fit"] == "flare-bottoms":
            score += 2
        else:
            score += 1    
            
    elif body_type == 'hourglass':
        if item["tops_fit"] in ["regular-fit-tops", 'fitted-tops', 'bodycon-tops']: 
            score += 2
        if item["neckline_type"] in ["high-neck", "v-neck", "shoulder-off", 'square-neck']:  
            score += 2
        if item["tops_length"] in ["thigh-length", "short"]:
            score += 2
        if item["style"] in ["feminine", "sophisticated"]:
            score += 2
        if item["sleeve_type"] == "straight-sleeve":
            score += 2
        if item["waist_type"] == "high-waist":
            score += 2    
        else:
            score += 1

    elif body_type == 'rectangle':
        if item["tops_fit"] in ["regular-fit-tops", 'oversized-tops']:
            score += 2
        if item["neckline_type"] in ["v-neck", "sweetheart-neck", "round-v-neck", "shoulder-off"]:  
            score += 2
        if item["tops_length"] in ["thigh-length", "long"]: 
            score -= 2
        if item["style"] in ["casuals"]:
            score += 2
        if item["sleeve_type"] in ['puff-sleeve', "flare-sleeve", "flutter-sleeve"]:
            score += 2
        if item["more_attributes"] in ["belted", "buttons"]:
            score += 2    
        if item["bottoms_fit"] == "flare-bottoms":
            score -= 2
        else:
            score += 1 
    return score

@app.route("/recommend", methods=["GET"])
def recommend():
    body_type = request.args.get("bodytype", "").lower()
    category = request.args.get("category", "").lower()

    if body_type not in ["hourglass", "rectangle", "apple"]:
        return jsonify({"error": "Invalid body type. Choose from hourglass, rectangle, or apple."}), 400

    # Apply scoring function
    df["suitability_score"] = df.apply(lambda row: score_clothing(row, body_type), axis=1)

    # Filter by category if provided
    if category:
        df_filtered = df[df["category"].str.lower() == category]
    else:
        df_filtered = df.copy()

    # Sort by suitability score (highest first) and get top 10 items
    df_sorted = df_filtered.sort_values(by="suitability_score", ascending=False).head(10)

    # Return barcode, image URL, and suitability score
    top_items = df_sorted[["barcode", "image_url_1", "suitability_score"]].to_dict(orient="records")

    return jsonify({"recommended_items": top_items})

if __name__ == "__main__":
    app.run(debug=True)
