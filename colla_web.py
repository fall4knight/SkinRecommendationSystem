from flask import Flask, jsonify
from colla_api import Recommender


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'What up guys! Welcome to the test web of skin recommendation system!'


@app.route('/theme/')
def theme():
    return 'Welcome to the theme!'


@app.route('/theme/<package_name>/')
def show_top3_recommendation(package_name):
    """
    如果没有键入需要输出的推荐个数
    则默认为推荐TOP 3
    """
    recommender = Recommender.build("skin_features.csv")
    package_list = [package_name]
    recommended_list = recommender.recommend(package_list, 3)
    return jsonify(recommended_list=recommended_list)

@app.route('/theme/<package_name>/<topn>/')
def show_recommendation(package_name, topn):
    """
    可以键入数字来决定输出的TOP N的个数
    """
    recommender = Recommender.build("skin_features.csv")
    package_list = [package_name]
    recommended_list = recommender.recommend(package_list, int(topn))
    return jsonify(recommended_list=recommended_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
