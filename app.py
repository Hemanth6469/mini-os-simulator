from flask import Flask, request, send_from_directory

app = Flask(
    __name__,
    static_folder='frontend'
)

# =====================================================
# HOME PAGE
# =====================================================

@app.route('/')
def home():

    return send_from_directory(
        'frontend',
        'index.html'
    )


# =====================================================
# STATIC FILES
# =====================================================

@app.route('/<path:path>')
def static_files(path):

    return send_from_directory(
        'frontend',
        path
    )


# =====================================================
# COMMON CPU RESULT PAGE
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

    body{
        background:#0f0f0f;
        color:white;
        font-family:Arial;
        text-align:center;
        padding:20px;
    }

    table{
        width:100%;
        margin-top:40px;
        border-collapse:collapse;
    }

    th,td{
        border:1px solid #444;
        padding:15px;
    }

    th{
        background:#333;
    }

    .cards{
        display:flex;
        justify-content:center;
        gap:25px;
        flex-wrap:wrap;
        margin-top:40px;
    }

    .card{
        background:#1f1f1f;
        padding:30px;
        border-radius:15px;
        min-width:250px;
    }

    .gantt{
        display:flex;
        justify-content:center;
        gap:20px;
        flex-wrap:wrap;
        margin-top:50px;
    }

    .gantt-block{
        background:#222;
        padding:25px;
        border-radius:15px;
        min-width:120px;
    }

    button{
        margin-top:50px;
        padding:15px 30px;
        font-size:20px;
        border:none;
        border-radius:10px;
        cursor:pointer;
    }

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
# COMMON DISK OUTPUT PAGE
# =====================================================

def disk_output(title, sequence, total_seek):

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

    <title>{title}</title>

    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <style>

    body{
        background:#0f0f0f;
        color:white;
        font-family:Arial;
        text-align:center;
        padding:20px;
    }

    .seek{
        font-size:35px;
        color:#00ff99;
        margin-top:30px;
    }

    .sequence{
        display:flex;
        justify-content:center;
        gap:20px;
        flex-wrap:wrap;
        margin-top:50px;
    }

    .block{
        background:#1f1f1f;
        padding:30px;
        border-radius:15px;
        min-width:100px;
        font-size:28px;
        transition:0.3s;
    }

    .block:hover{
        transform:scale(1.08);
    }

    button{
        margin-top:50px;
        padding:15px 30px;
        font-size:18px;
        border:none;
        border-radius:10px;
        cursor:pointer;
    }

    </style>

    </head>

    <body>

    <h1>{title}</h1>

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
# DISK FCFS
# =====================================================

@app.route('/run_disk_fcfs', methods=['POST'])
def run_disk_fcfs():

    requests = list(
        map(
            int,
            request.form['requests'].split()
        )
    )

    head = int(request.form['head'])

    sequence = [head] + requests

    total_seek = 0

    for i in range(len(sequence)-1):

        total_seek += abs(
            sequence[i+1] - sequence[i]
        )

    return disk_output(
        "FCFS Disk Scheduling Result",
        sequence,
        total_seek
    )


# =====================================================
# DISK SSTF
# =====================================================

@app.route('/run_disk_sstf', methods=['POST'])
def run_disk_sstf():

    requests = list(
        map(
            int,
            request.form['requests'].split()
        )
    )

    head = int(request.form['head'])

    sequence = [head]

    total_seek = 0

    while requests:

        closest = min(
            requests,
            key=lambda x: abs(x - head)
        )

        total_seek += abs(
            closest - head
        )

        head = closest

        sequence.append(head)

        requests.remove(closest)

    return disk_output(
        "SSTF Disk Scheduling Result",
        sequence,
        total_seek
    )


# =====================================================
# DISK SCAN
# =====================================================

@app.route('/run_disk_scan', methods=['POST'])
def run_disk_scan():

    requests = list(
        map(
            int,
            request.form['requests'].split()
        )
    )

    head = int(request.form['head'])

    disk_size = 200

    left = []
    right = []

    for req in requests:

        if req < head:
            left.append(req)
        else:
            right.append(req)

    left.sort()
    right.sort()

    sequence = [head]

    total_seek = 0
    current = head

    for req in right:

        total_seek += abs(req - current)
        current = req
        sequence.append(req)

    total_seek += abs((disk_size - 1) - current)

    current = disk_size - 1

    sequence.append(current)

    left.reverse()

    for req in left:

        total_seek += abs(req - current)
        current = req
        sequence.append(req)

    return disk_output(
        "SCAN Disk Scheduling Result",
        sequence,
        total_seek
    )


# =====================================================
# DISK C-SCAN
# =====================================================

@app.route('/run_disk_cscan', methods=['POST'])
def run_disk_cscan():

    requests = list(
        map(
            int,
            request.form['requests'].split()
        )
    )

    head = int(request.form['head'])

    disk_size = 200

    left = []
    right = []

    for req in requests:

        if req < head:
            left.append(req)
        else:
            right.append(req)

    left.sort()
    right.sort()

    sequence = [head]

    total_seek = 0
    current = head

    for req in right:

        total_seek += abs(req - current)
        current = req
        sequence.append(req)

    total_seek += abs((disk_size - 1) - current)

    current = disk_size - 1

    sequence.append(current)

    total_seek += current

    current = 0

    sequence.append(current)

    for req in left:

        total_seek += abs(req - current)
        current = req
        sequence.append(req)

    return disk_output(
        "C-SCAN Disk Scheduling Result",
        sequence,
        total_seek
    )


# =====================================================
# DISK LOOK
# =====================================================

@app.route('/run_disk_look', methods=['POST'])
def run_disk_look():

    requests = list(
        map(
            int,
            request.form['requests'].split()
        )
    )

    head = int(request.form['head'])

    left = []
    right = []

    for req in requests:

        if req < head:
            left.append(req)
        else:
            right.append(req)

    left.sort()
    right.sort()

    sequence = [head]

    total_seek = 0
    current = head

    for req in right:

        total_seek += abs(req - current)
        current = req
        sequence.append(req)

    left.reverse()

    for req in left:

        total_seek += abs(req - current)
        current = req
        sequence.append(req)

    return disk_output(
        "LOOK Disk Scheduling Result",
        sequence,
        total_seek
    )


# =====================================================
# DISK C-LOOK
# =====================================================

@app.route('/run_disk_clook', methods=['POST'])
def run_disk_clook():

    requests = list(
        map(
            int,
            request.form['requests'].split()
        )
    )

    head = int(request.form['head'])

    left = []
    right = []

    for req in requests:

        if req < head:
            left.append(req)
        else:
            right.append(req)

    left.sort()
    right.sort()

    sequence = [head]

    total_seek = 0
    current = head

    for req in right:

        total_seek += abs(req - current)
        current = req
        sequence.append(req)

    if left:

        total_seek += abs(current - left[0])

        current = left[0]

        sequence.append(current)

    for req in left[1:]:

        total_seek += abs(req - current)

        current = req

        sequence.append(req)

    return disk_output(
        "C-LOOK Disk Scheduling Result",
        sequence,
        total_seek
    )


# =====================================================
# MAIN
# =====================================================

if __name__ == '__main__':

    app.run(debug=True)