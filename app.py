from flask import Flask, render_template,request
import pickle

cafes = pickle.load(open('model/cafe_list.pkl','rb'))
similarity= pickle.load(open('model/similarity.pkl','rb'))

def recommend(cafe):
    index = cafes[cafes['title'] == cafe].index[0]
    distances = sorted(list(enumerate(similarity[index])),vreverse=True,key=lambda x:x[1])
    recommended_cafe_name=[]
    # recommendeed_cafe_poster=[]

    for i in distances[1:6]:
        recommended_cafe_name.append(cafes.iloc[i[0]].title)

    return recommended_cafe_name





app = Flask(__name__)

# Create navbar and footer routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/searchcafe',methods=['GET','POST'])
def searchcafe():

    cafe_list=cafes['title'].values

    if request.method =="POST":
        try:
            if request.form['cafes']:
                cafe_name=request.form['cafes']
                # print(cafe_name)
                recommended_cafe_name=recommend(cafe_name)

                return render_template('searchcafe.html',cafe_name=recommended_cafe_name, cafe_list=cafe_list)
        
        except Exception as e:
            error={'error':e}
            return render_template('searchcafe.html',cafe_list=cafe_list)
    else:
        return render_template('searchcafe.html',cafe_list=cafe_list)                   
    


if __name__ == '__main__':
    app.run(debug=True)
