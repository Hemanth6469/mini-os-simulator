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

    button{{
        margin-top:70px;
        margin-bottom:50px;
        padding:18px 35px;
        font-size:22px;
        border:none;
        border-radius:12px;
        cursor:pointer;
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

        <circle
            cx="{x}"
            cy="{y}"
            r="10"
            fill="white"
        />

        <text
            x="{x-15}"
            y="{y-18}">

            {value}

        </text>

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
# MAIN
# =====================================================

if __name__ == '__main__':

    app.run(debug=True)