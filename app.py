from flask import Flask, request, jsonify
import pickle
from urllib.parse import urlparse

app = Flask(__name__)

# Load the trained models
models = {}
model_names = ['rf_model.pkl', 'gb_model.pkl', 'knn_model.pkl']

for model_name in model_names:
    with open(model_name, 'rb') as file:
        models[model_name.split('_')[0]] = pickle.load(file)

# Function to extract features from URL
def extract_features(url):
    parsed_url = urlparse(url)
    
    features = {}
    
    # URL Length
    url_length = len(url)
    features['URL_Length'] = url_length
    
    # Domain Features
    domain = parsed_url.netloc
    features['SpecialChars'] = sum(1 for char in domain if not char.isalnum())
    features['Symbols'] = sum(1 for char in url if not char.isalnum() and char not in ['/', '.', '-', '_'])
    features['Chars'] = sum(1 for char in url if char.isalpha())
    features['Numbers'] = sum(1 for char in url if char.isdigit())
    features['domain_length'] = len(domain)
    features['subdomains_count'] = domain.count('.')
    
    # Path Features
    path = parsed_url.path
    features['path_length'] = len(path)
    features['path_segments_count'] = path.count('/') + 1
    features['keywords_in_path'] = any(keyword in path.lower() for keyword in ['login', 'admin', 'malware'])
    
    # Query Features
    query = parsed_url.query
    features['query_params_count'] = len(query.split('&')) if query else 0
    
    # Protocol Features
    features['uses_https'] = int(parsed_url.scheme == 'https')
    
    return features

# Define a route for the classification endpoint
@app.route('/classify', methods=['POST'])
def classify_url():
    try:
        # Get the URL from the request
        url = request.json['url']
        
        # Extract features from the URL
        features = extract_features(url)
        
        # Convert int32 values to Python integers
        features = {key: int(value) for key, value in features.items()}
        
        # Make predictions using the loaded models
        predictions = {}
        for model_name, model in models.items():
            prediction = model.predict([list(features.values())])[0]
            # Convert prediction to native Python data type
            prediction = int(prediction)
            predictions[model_name] = prediction
        
        # Prepare response JSON
        response = {'url': url, 'predictions': predictions}
        
        return jsonify(response), 200
    except Exception as e:
        error_message = str(e)
        return jsonify({'error': error_message}), 400

if __name__ == '__main__':
    app.run(debug=True)
