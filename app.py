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
# COMMON RESULT PAGE
# =====================================================

def generate_cpu_page(title, at, bt, wt, tat):

    n = len(bt)

    avg_wt = sum(wt) / n
    avg_tat = sum(tat) / n

    table = ""

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

    <title>{title}</title>

    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <style>

    body{{
        background:#0f0f0f;
        color:white;
        font-family:Arial;
        text-align:center;
        padding:20px;
    }}

    h1{{
        margin-top:20px;
    }}

    table{{
        width:100%;
        margin-top:40px;
        border-collapse:collapse;
    }}

    th,td{{
        border:1px solid #444;
        padding:15px;
    }}

    th{{
        background:#333;
    }}

    .cards{{
        display:flex;
        justify-content:center;
        gap:25px;
        flex-wrap:wrap;
        margin-top:40px;
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
        flex-wrap:wrap;
        margin-top:50px;
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

    <h1>{title}</h1>

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
# FCFS
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

    return generate_cpu_page(
        "FCFS Scheduling Result",
        at,
        bt,
        wt,
        tat
    )


# =====================================================
# SJF
# =====================================================

@app.route('/run_sjf', methods=['POST'])
def run_sjf():

    n = int(request.form['n'])

    at = []
    bt = []

    for i in range(n):
        at.append(int(request.form[f'at{i}']))
        bt.append(int(request.form[f'bt{i}']))

    processes = []

    for i in range(n):
        processes.append((bt[i], at[i], i))

    processes.sort()

    wt = [0] * n
    tat = [0] * n

    current = 0

    for bt_val, at_val, idx in processes:

        wt[idx] = current
        tat[idx] = wt[idx] + bt_val

        current += bt_val

    return generate_cpu_page(
        "SJF Scheduling Result",
        at,
        bt,
        wt,
        tat
    )


# =====================================================
# ROUND ROBIN
# =====================================================

@app.route('/run_rr', methods=['POST'])
def run_rr():

    n = int(request.form['n'])

    tq = int(request.form['tq'])

    at = []
    bt = []

    for i in range(n):
        at.append(int(request.form[f'at{i}']))
        bt.append(int(request.form[f'bt{i}']))

    rem = bt.copy()

    wt = [0] * n
    tat = [0] * n

    time = 0

    while True:

        done = True

        for i in range(n):

            if rem[i] > 0:

                done = False

                if rem[i] > tq:

                    time += tq
                    rem[i] -= tq

                else:

                    time += rem[i]

                    wt[i] = time - bt[i]

                    rem[i] = 0

        if done:
            break

    for i in range(n):
        tat[i] = wt[i] + bt[i]

    return generate_cpu_page(
        "Round Robin Result",
        at,
        bt,
        wt,
        tat
    )


# =====================================================
# PRIORITY
# =====================================================

@app.route('/run_priority', methods=['POST'])
def run_priority():

    n = int(request.form['n'])

    at = []
    bt = []
    pr = []

    for i in range(n):

        at.append(int(request.form[f'at{i}']))
        bt.append(int(request.form[f'bt{i}']))
        pr.append(int(request.form[f'pr{i}']))

    processes = []

    for i in range(n):
        processes.append((pr[i], at[i], bt[i], i))

    processes.sort()

    wt = [0] * n
    tat = [0] * n

    current = 0

    for priority, at_val, bt_val, idx in processes:

        wt[idx] = current
        tat[idx] = wt[idx] + bt_val

        current += bt_val

    return generate_cpu_page(
        "Priority Scheduling Result",
        at,
        bt,
        wt,
        tat
    )


# =====================================================
# MAIN
# =====================================================

if __name__ == '__main__':
    app.run(debug=True)