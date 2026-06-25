from flask import Flask, request

app = Flask(__name__)


# =====================================================
# DISK RESULT PAGE WITH GRAPH
# =====================================================

def generate_disk_page(title, sequence, total_seek):

    graph_points = ""

    x = 100

    for value in sequence:

        y = 350 - value

        graph_points += f"{x},{y} "

        x += 140

    blocks = ""

    for i in range(len(sequence)-1):

        blocks += f"""

        <div class="block">

            <div class="disk-number">

                {sequence[i]}

            </div>

            <div class="arrow">

                ⬇

            </div>

            <div class="disk-number">

                {sequence[i+1]}

            </div>

        </div>
        """

    html = f"""

    <html>

    <head>

    <title>{title}</title>

    <style>

    body{{
        background:#0f0f0f;
        color:white;
        font-family:Arial;
        text-align:center;
        margin:0;
        padding:0;
    }}

    h1{{
        margin-top:30px;
        font-size:55px;
    }}

    .seek{{
        font-size:42px;
        margin-top:40px;
        color:#00ff99;
        font-weight:bold;
    }}

    .graph-container{{
        margin-top:60px;
        overflow-x:auto;
        padding:20px;
    }}

    svg{{
        background:#181818;
        border-radius:20px;
        padding:30px;

        box-shadow:0px 0px 25px rgba(255,255,255,0.08);
    }}

    .line{{
        animation:drawLine 2s ease;
    }}

    @keyframes drawLine{{
        from{{
            opacity:0;
        }}

        to{{
            opacity:1;
        }}
    }}

    .sequence{{
        display:flex;
        justify-content:center;
        gap:25px;
        flex-wrap:wrap;
        margin-top:70px;
    }}

    .block{{
        background:#242424;

        padding:30px;

        border-radius:18px;

        min-width:110px;

        transition:0.4s;

        box-shadow:0px 0px 15px rgba(255,255,255,0.05);
    }}

    .block:hover{{
        transform:translateY(-10px) scale(1.05);

        box-shadow:0px 0px 30px rgba(255,255,255,0.18);
    }}

    .disk-number{{
        font-size:28px;
        font-weight:bold;
    }}

    .arrow{{
        margin:15px 0;
        font-size:28px;
        color:#00ff99;
    }}

    text{{
        fill:white;
        font-size:18px;
        font-weight:bold;
    }}

    .point{{
        animation:pop 1s ease;
    }}

    @keyframes pop{{
        from{{
            transform:scale(0);
            opacity:0;
        }}

        to{{
            transform:scale(1);
            opacity:1;
        }}
    }}

    button{{
        margin-top:70px;
        margin-bottom:50px;

        padding:18px 35px;

        font-size:22px;

        border:none;

        border-radius:12px;

        cursor:pointer;

        transition:0.4s;
    }}

    button:hover{{
        transform:scale(1.08);

        box-shadow:0px 0px 25px rgba(255,255,255,0.25);
    }}

    </style>

    </head>

    <body>

    <h1>{title}</h1>

    <div class="seek">

        Total Seek Time = {total_seek}

    </div>

    <div class="graph-container">

    <svg width="1800" height="500">

        <!-- AXIS -->

        <line
            x1="60"
            y1="380"
            x2="1700"
            y2="380"
            stroke="white"
            stroke-width="2"
        />

        <line
            x1="60"
            y1="40"
            x2="60"
            y2="380"
            stroke="white"
            stroke-width="2"
        />

        <!-- GRAPH LINE -->

        <polyline
            class="line"
            fill="none"
            stroke="#00ff99"
            stroke-width="5"
            points="{graph_points}"
        />

    """

    x = 100

    for value in sequence:

        y = 350 - value

        html += f"""

        <!-- POINT -->

        <circle
            class="point"
            cx="{x}"
            cy="{y}"
            r="10"
            fill="white"
        />

        <!-- LABEL -->

        <text
            x="{x-15}"
            y="{y-18}">

            {value}

        </text>

        <!-- X LABEL -->

        <text
            x="{x-10}"
            y="420">

            {value}

        </text>
        """

        x += 140

    html += f"""

    </svg>

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

    return html


# =====================================================
# HOME
# =====================================================

@app.route('/')
def home():

    return "<h1>Disk Scheduling Simulator Running</h1>"


# =====================================================
# FCFS DISK
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

        total_seek += abs(
            sequence[i+1] - sequence[i]
        )

    return generate_disk_page(
        "FCFS Disk Scheduling Result",
        sequence,
        total_seek
    )


# =====================================================
# SSTF DISK
# =====================================================

@app.route('/run_disk_sstf', methods=['POST'])
def run_disk_sstf():

    requests = list(map(
        int,
        request.form['requests'].split()
    ))

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

    return generate_disk_page(
        "SSTF Disk Scheduling Result",
        sequence,
        total_seek
    )


# =====================================================
# SCAN DISK
# =====================================================

@app.route('/run_disk_scan', methods=['POST'])
def run_disk_scan():

    requests = list(map(
        int,
        request.form['requests'].split()
    ))

    head = int(request.form['head'])

    disk_size = 200

    left = []
    right = []

    for req in requests:

        if req < head:
            left.append(req)
        else:
            right.append(req)

    left.sort(reverse=True)
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

    for req in left:

        total_seek += abs(req - current)

        current = req

        sequence.append(req)

    return generate_disk_page(
        "SCAN Disk Scheduling Result",
        sequence,
        total_seek
    )


# =====================================================
# C-SCAN DISK
# =====================================================

@app.route('/run_disk_cscan', methods=['POST'])
def run_disk_cscan():

    requests = list(map(
        int,
        request.form['requests'].split()
    ))

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

    return generate_disk_page(
        "C-SCAN Disk Scheduling Result",
        sequence,
        total_seek
    )


# =====================================================
# LOOK DISK
# =====================================================

@app.route('/run_disk_look', methods=['POST'])
def run_disk_look():

    requests = list(map(
        int,
        request.form['requests'].split()
    ))

    head = int(request.form['head'])

    left = []
    right = []

    for req in requests:

        if req < head:
            left.append(req)
        else:
            right.append(req)

    left.sort(reverse=True)
    right.sort()

    sequence = [head]

    total_seek = 0

    current = head

    for req in right:

        total_seek += abs(req - current)

        current = req

        sequence.append(req)

    for req in left:

        total_seek += abs(req - current)

        current = req

        sequence.append(req)

    return generate_disk_page(
        "LOOK Disk Scheduling Result",
        sequence,
        total_seek
    )


# =====================================================
# C-LOOK DISK
# =====================================================

@app.route('/run_disk_clook', methods=['POST'])
def run_disk_clook():

    requests = list(map(
        int,
        request.form['requests'].split()
    ))

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

    return generate_disk_page(
        "C-LOOK Disk Scheduling Result",
        sequence,
        total_seek
    )


# =====================================================
# MAIN
# =====================================================

if __name__ == '__main__':

    app.run(debug=True)