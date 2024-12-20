from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import joblib
import numpy as np
import os

app = Flask(__name__, static_folder='static', static_url_path='/')
CORS(app)

# 加载模型
try:
    model_path = os.path.join(os.path.dirname(__file__), 'iris_model.pkl')
    model = joblib.load(model_path)
except FileNotFoundError:
    raise RuntimeError("Model file 'iris_model.pkl' not found. Please upload the model file.")
except Exception as e:
    raise RuntimeError(f"An error occurred while loading the model: {str(e)}")


# 路由：提供前端网页
@app.route('/')
def home():
    return send_from_directory(app.static_folder, 'index.html')


# 路由：提供预测功能
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        if 'features' not in data:
            return jsonify({'error': 'Invalid input, "features" is required'}), 400

        features = np.array(data['features']).reshape(1, -1)
        prediction = model.predict(features)
        return jsonify({'prediction': int(prediction[0])})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# 健康检查接口
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'}), 200


# 禁用静态文件缓存
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
