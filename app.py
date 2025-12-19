from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

def prediction(lst):
    filename = 'Model/predictor.pickle'
    with open(filename, 'rb') as file:
        model = pickle.load(file)
    pred_value = model.predict([lst])
    return pred_value[0]

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        ram = int(request.form['ram'])
        weight = float(request.form['weight'])
        company = request.form['company'].lower()
        typename = request.form['typename'].lower()
        opsys = request.form['opsys'].lower()
        cpu = request.form['cpuname'].lower()
        gpu = request.form['gpuname'].lower()
        
        touchscreen = 1 if request.form.get('touchscreen') else 0
        ips = 1 if request.form.get('ips') else 0
        
        feature_list = [ram, weight, touchscreen, ips]

        company_list = ['acer', 'apple', 'asus', 'dell', 'hp', 'lenovo', 'msi', 'other', 'samsung', 'toshiba']
        typename_list = ['2 in 1 convertible', 'gaming', 'netbook', 'notebook', 'ultrabook', 'workstation']
        opsys_list = ['android', 'chrome os', 'linux', 'mac', 'no os', 'windows']
        cpu_list = ['amd', 'intel core i3', 'intel core i5', 'intel core i7', 'other']
        gpu_list = ['amd', 'intel', 'nvidia']

        def traverse(lst, value):
            for item in lst:
                feature_list.append(1 if item == value else 0)

        traverse(company_list, company)
        traverse(typename_list, typename)
        traverse(opsys_list, opsys)
        traverse(cpu_list, cpu)
        traverse(gpu_list, gpu)

        # Ensure feature count matches model input
        feature_list = feature_list[:29]

        EUR_to_LKR = 380  # Current exchange rate
        pred = prediction(feature_list) * EUR_to_LKR
        
        return render_template('index.html', pred_value=pred)

    return render_template('index.html', pred_value=None)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
