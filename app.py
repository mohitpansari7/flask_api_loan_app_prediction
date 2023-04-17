from flask import Flask, request
import pickle

app = Flask(__name__)

model_pickle = open('./Artifacts/classifier.pkl', 'rb')
clf = pickle.load(model_pickle)


@app.route('/ping', methods=['GET'])
def ping():
    return {"message":"Hi, Server is up and running"}

@app.route('/params', methods=['GET'])
def getParams():
    parameters = {
        "Gender":"<Male/Female>",
        "Married":"<Married/Unmarried>",
        "ApplicantIncome":5000,
        "Credit_History":"Cleared Debts",
        "LoanAmount":50000
    }
    return parameters

@app.route('/predict', methods=['POST'])
def prediction():
    print(request.get_json())
    loan_req = request.get_json()

    if loan_req['Gender'] == 'Male':
        Gender = 0
    else:
        Gender = 1

    if loan_req['Married'] == 'Married':
        Married = 1
    else:
        Married = 0

    if loan_req['Credit_History'] == 'Unclear Debts':
        Credit_History = 0
    else:
        Credit_History = 1
    
    ApplicantIncome = loan_req['ApplicantIncome']
    LoanAmount = loan_req['LoanAmount']

    result = clf.predict([[Gender, Married, ApplicantIncome, LoanAmount, Credit_History]])
    print(result)
    if result == 0:
        pred = 'Rejected'
    else:
        pred = 'Approved'

    return {"Loan Status":pred}


