from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():

    return """

    <h1>

    Mini OS Simulator Running ✅

    </h1>
    """

@app.route('/run_fcfs', methods=['POST'])
def run_fcfs():

    return """

    <h1>

    FCFS Working ✅

    </h1>
    """

if __name__ == '__main__':

    app.run(debug=True)