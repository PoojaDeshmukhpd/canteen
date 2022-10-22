from flask import Flask, render_template,request
import pickle as pk
import numpy as np

popular_df = pk.load(open('popular.pkl', 'rb'))
app = Flask(__name__)
pt=pk.load(open('pt.pkl', 'rb'))
books=pk.load(open('books.pkl', 'rb'))
simalarity_score=pk.load(open('simalarity_score.pkl', 'rb'))
@app.route('/')
def index():
    return render_template('index.html',
                           name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           rating=list(popular_df['avg_rating'].values)
                           )
@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')


@app.route('/recommend_books', methods=['POST'])
def recommend():
    # index from book nam

    user=request.form.get('user')
    index = np.where(pt.index == user)[0][0]
    similar_items = sorted(list(enumerate(simalarity_score[index])), key=lambda x: x[1], reverse=True)[1:6]
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Author')['Book-Author'].values))

        data.append(item)
    print(data)

    return render_template('recommend.html',data=data)

if __name__ == '__main__':
    app.run(debug=True)
