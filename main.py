
# coding: utf-8

# In[ ]:


from flask import Flask , jsonify , request , render_template , url_for , _request_ctx_stack
import graduation
#sc=SparkContext()
app = Flask(__name__)

@app.before_request
def before_request():
    method = request.form.get('_method', '').upper()
    if method:
        request.environ['REQUEST_METHOD'] = method
        ctx = _request_ctx_stack.top
        ctx.url_adapter.default_method = method
        assert request.method == method

#post /search 搜尋目標
@app.route('/search' , methods=['POST'])
def submit():
    print(request.form.get('account'))
    returnData = graduation.main(request.form.get('account'),request.form.get('password'),request.form.get('cpe_num'))
    if returnData == 4044444:
        return render_template('wrongInfo.html', data='帳號或密碼錯誤！')
    else:
        return render_template('result.html', data=returnData)


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()


