from flask import Flask, request, send_from_directory

app = Flask(
    __name__,
    static_folder='frontend'
)

# =====================================================
# FRONTEND ROUTES
# =====================================================

@app.route('/')
def home():
    return send_from_directory('frontend', 'index.html')


@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('frontend', path)


# =====================================================
# FCFS CPU SCHEDULING
# =====================================================

@app.route('/run_fcfs', methods=['POST'])
def run_fcfs():

    n = int(request.form['n'])

    at = []
    bt = []

    for i in range(n):
        at.append(int(request.form[f'at{i}']))
        bt.append(int(request.form[f'bt{i}']))

    wt = [0] * n
    tat = [0] * n

    for i in range(1, n):
        wt[i] = wt[i-1] + bt[i-1]

    for i in range(n):
        tat[i] = wt[i] + bt[i]

    avg_wt = sum(wt) / n
    avg_tat = sum(tat) / n

    gantt = ""

    current = 0

    for i in range(n):

        end = current + bt[i]

        gantt += f"""
        <div class="gantt-block">
            <h3>P{i+1}</h3>
            <p>{current} - {end}</p>
        </div>
        """

        current = end

    table = ""

    for i in range(n):

        table += f"""
        <tr>
            <td>P{i+1}</td>
            <td>{at[i]}</td>
            <td>{bt[i]}</td>
            <td>{wt[i]}</td>
            <td>{tat[i]}</td>
        </tr>
        """

    return f"""

    <html>

    <head>

    <title>FCFS Result</title>

    <style>

    body{{
        background:#0f0f0f;
        color:white;
        font-family:Arial;
        text-align:center;
    }}

    table{{
        width:90%;
        margin:auto;
        margin-top:40px;
        border-collapse:collapse;
    }}

    th,td{{
        border:1px solid #444;
        padding:15px;
        font-size:22px;
    }}

    th{{
        background:#333;
    }}

    .cards{{
        display:flex;
        justify-content:center;
        gap:30px;
        margin-top:40px;
        flex-wrap:wrap;
    }}

    .card{{
        background:#1f1f1f;
        padding:30px;
        border-radius:15px;
        min-width:250px;
    }}

    .gantt{{
        display:flex;
        justify-content:center;
        gap:20px;
        margin-top:50px;
        flex-wrap:wrap;
    }}

    .gantt-block{{
        background:#222;
        padding:25px;
        border-radius:15px;
        min-width:120px;
    }}

    button{{
        margin-top:50px;
        padding:15px 30px;
        font-size:20px;
        border:none;
        border-radius:10px;
        cursor:pointer;
    }}

    </style>

    </head>

    <body>

    <h1>FCFS Scheduling Result</h1>

    <div class="cards">

        <div class="card">
            <h2>Average Waiting Time</h2>
            <h1>{avg_wt:.2f}</h1>
        </div>

        <div class="card">
            <h2>Average Turnaround Time</h2>
            <h1>{avg_tat:.2f}</h1>
        </div>

    </div>

    <table>

        <tr>
            <th>Process</th>
            <th>AT</th>
            <th>BT</th>
            <th>WT</th>
            <th>TAT</th>
        </tr>

        {table}

    </table>

    <h1>Gantt Chart</h1>

    <div class="gantt">

        {gantt}

    </div>

    <button onclick="history.back()">
        Back
    </button>

    </body>

    </html>
    """


# =====================================================
# DISK FCFS
# =====================================================

@app.route('/run_disk_fcfs', methods=['POST'])
def run_disk_fcfs():

    requests = list(map(
        int,
        request.form['requests'].split()
    ))

    head = int(request.form['head'])

    sequence = [head] + requests

    total_seek = 0

    for i in range(len(sequence)-1):
        total_seek += abs(sequence[i+1] - sequence[i])

    blocks = ""

    for value in sequence:

        blocks += f"""
        <div class="block">
            {value}
        </div>
        """

    return f"""

    <html>

    <head>

    <title>Disk FCFS Result</title>

    <style>

    body{{
        background:#0f0f0f;
        color:white;
        font-family:Arial;
        text-align:center;
    }}

    .seek{{
        margin-top:40px;
        font-size:40px;
        color:#00ff99;
    }}

    .sequence{{
        display:flex;
        justify-content:center;
        gap:20px;
        flex-wrap:wrap;
        margin-top:60px;
    }}

    .block{{
        background:#1f1f1f;
        padding:30px;
        border-radius:15px;
        min-width:100px;
        font-size:28px;
    }}

    button{{
        margin-top:60px;
        padding:15px 30px;
        font-size:20px;
        border:none;
        border-radius:10px;
        cursor:pointer;
    }}

    </style>

    </head>

    <body>

    <h1>FCFS Disk Scheduling Result</h1>

    <div class="seek">

        Total Seek Time = {total_seek}

    </div>

    <div class="sequence">

        {blocks}

    </div>

    <button onclick="history.back()">
        Back
    </button>

    </body>

    </html>
    """


# =====================================================
# MAIN
# =====================================================

if __name__ == '__main__':
    app.run(debug=True)