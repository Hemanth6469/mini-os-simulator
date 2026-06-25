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

    return send_from_directory(
        'frontend',
        'index.html'
    )

@app.route('/<path:path>')
def static_files(path):

    return send_from_directory(
        'frontend',
        path
    )


# =====================================================
# DISK RESULT PAGE
# =====================================================

def generate_disk_page(title, sequence, total_seek):

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
    }}

    h1{{
        margin-top:30px;
        font-size:55px;
    }}

    .seek{{
        font-size:40px;
        margin-top:40px;
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
        background:#1c1c1c;

        padding:30px;

        border-radius:15px;

        min-width:100px;

        transition:0.4s;
    }}

    .block:hover{{
        transform:translateY(-10px) scale(1.05);
    }}

    button{{
        margin-top:60px;

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

    <div class="sequence">
    """

    for value in sequence:

        html += f"""

        <div class="block">

            {value}

        </div>
        """

    html += """

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