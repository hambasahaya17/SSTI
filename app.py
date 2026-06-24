from flask import Flask, request, render_template_string, render_template, session
import os
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# Flag disimpan di environment variable
FLAG = os.environ.get("FLAG", "LKSP{ssT1_1s_d4ng3r0us_t3mpl4t3_1nj3ct10n}")

# Template halaman utama
HOME_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GreetBot - Personal Greeting Service</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@300;400;600&display=swap');

        * { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            background: #0d0f14;
            color: #c9d1d9;
            font-family: 'Inter', sans-serif;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 2rem;
        }

        .terminal-window {
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 8px;
            width: 100%;
            max-width: 640px;
            overflow: hidden;
            box-shadow: 0 0 40px rgba(88, 166, 255, 0.08);
        }

        .terminal-bar {
            background: #21262d;
            padding: 12px 16px;
            display: flex;
            align-items: center;
            gap: 8px;
            border-bottom: 1px solid #30363d;
        }

        .dot { width: 12px; height: 12px; border-radius: 50%; }
        .dot-red { background: #ff5f57; }
        .dot-yellow { background: #febc2e; }
        .dot-green { background: #28c840; }

        .terminal-title {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.75rem;
            color: #8b949e;
            margin-left: auto;
            margin-right: auto;
        }

        .terminal-body { padding: 2rem; }

        .prompt-line {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
            color: #58a6ff;
            margin-bottom: 1.5rem;
        }

        .prompt-line span { color: #3fb950; }

        h1 {
            font-size: 1.4rem;
            font-weight: 600;
            color: #e6edf3;
            margin-bottom: 0.4rem;
        }

        .subtitle {
            font-size: 0.85rem;
            color: #8b949e;
            margin-bottom: 2rem;
            font-family: 'JetBrains Mono', monospace;
        }

        .form-group { margin-bottom: 1.2rem; }

        label {
            display: block;
            font-size: 0.78rem;
            color: #8b949e;
            font-family: 'JetBrains Mono', monospace;
            margin-bottom: 0.5rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        input[type="text"] {
            width: 100%;
            background: #0d1117;
            border: 1px solid #30363d;
            border-radius: 6px;
            padding: 0.7rem 1rem;
            color: #e6edf3;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.9rem;
            outline: none;
            transition: border-color 0.2s;
        }

        input[type="text"]:focus { border-color: #58a6ff; }
        input[type="text"]::placeholder { color: #484f58; }

        button {
            width: 100%;
            background: #238636;
            color: #fff;
            border: none;
            border-radius: 6px;
            padding: 0.75rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.9rem;
            cursor: pointer;
            transition: background 0.2s;
            margin-top: 0.5rem;
        }

        button:hover { background: #2ea043; }

        .hint-box {
            margin-top: 1.5rem;
            background: #161b22;
            border: 1px solid #30363d;
            border-left: 3px solid #f0883e;
            border-radius: 4px;
            padding: 1rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.78rem;
            color: #8b949e;
        }

        .hint-box .hint-title {
            color: #f0883e;
            font-weight: 700;
            margin-bottom: 0.5rem;
            font-size: 0.7rem;
            text-transform: uppercase;
            letter-spacing: 0.1em;
        }

        .source-link {
            display: inline-block;
            margin-top: 1rem;
            color: #58a6ff;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.78rem;
            text-decoration: none;
        }

        .source-link:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="terminal-window">
        <div class="terminal-bar">
            <div class="dot dot-red"></div>
            <div class="dot dot-yellow"></div>
            <div class="dot dot-green"></div>
            <span class="terminal-title">greetbot-service — bash</span>
        </div>
        <div class="terminal-body">
            <div class="prompt-line"><span>user@greetbot</span>:~$ ./greet.py --interactive</div>
            <h1>GreetBot v1.3</h1>
            <p class="subtitle"># personal greeting generator service</p>

            <form method="POST" action="/greet">
                <div class="form-group">
                    <label>Your Name</label>
                    <input type="text" name="name" placeholder="Enter your name..." autocomplete="off">
                </div>
                <button type="submit">Generate Greeting →</button>
            </form>

            <div class="hint-box">
                <div class="hint-title">⚠ Challenge Info</div>
                Aplikasi ini menggunakan template engine untuk memformat greeting. 
                Dapatkah kamu menemukan flag yang tersembunyi di environment variables?
                <br><br>
                <code>FLAG disimpan di: os.environ["FLAG"]</code>
            </div>

            <a class="source-link" href="/source">📄 Lihat source code →</a>
        </div>
    </div>
</body>
</html>
"""

SOURCE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Source Code - GreetBot</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;600&display=swap');
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background: #0d0f14;
            color: #c9d1d9;
            font-family: 'Inter', sans-serif;
            padding: 2rem;
        }
        .container { max-width: 800px; margin: 0 auto; }
        h1 { color: #e6edf3; margin-bottom: 0.5rem; font-size: 1.3rem; }
        .back { color: #58a6ff; font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; text-decoration: none; display: inline-block; margin-bottom: 1.5rem; }
        .back:hover { text-decoration: underline; }
        pre {
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 1.5rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.82rem;
            overflow-x: auto;
            line-height: 1.7;
            color: #e6edf3;
        }
        .kw { color: #ff7b72; }
        .fn { color: #d2a8ff; }
        .st { color: #a5d6ff; }
        .cm { color: #8b949e; font-style: italic; }
        .num { color: #79c0ff; }
    </style>
</head>
<body>
    <div class="container">
        <a class="back" href="/">← Kembali ke GreetBot</a>
        <h1>📄 app.py — Source Code</h1>
        <br>
        <pre><span class="kw">from</span> flask <span class="kw">import</span> Flask, request, render_template_string
<span class="kw">import</span> os

app = Flask(__name__)

FLAG = os.environ.get(<span class="st">"FLAG"</span>, <span class="st">"CTF{placeholder}"</span>)

<span class="cm"># ~~~ Endpoint utama ~~~</span>
<span class="kw">@app</span>.route(<span class="st">"/greet"</span>, methods=[<span class="st">"POST"</span>])
<span class="kw">def</span> <span class="fn">greet</span>():
    name = request.form.get(<span class="st">"name"</span>, <span class="st">""</span>)

    <span class="cm"># WARN: langsung dirender tanpa sanitasi!</span>
    template = <span class="st">f"&lt;h2&gt;Hello, {name}!&lt;/h2&gt;"</span>

    <span class="kw">return</span> render_template_string(template)

<span class="kw">if</span> __name__ == <span class="st">"__main__"</span>:
    app.run()</pre>
    </div>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(HOME_TEMPLATE)


@app.route("/source")
def source():
    return render_template_string(SOURCE_TEMPLATE)


@app.route("/greet", methods=["POST"])
def greet():
    name = request.form.get("name", "")

    if not name:
        return render_template_string(HOME_TEMPLATE)

    # VULNERABLE: input langsung dimasukkan ke template tanpa sanitasi
    template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>GreetBot - Result</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@300;400;600&display=swap');
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            background: #0d0f14;
            color: #c9d1d9;
            font-family: 'Inter', sans-serif;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 2rem;
        }}
        .card {{
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 2.5rem;
            max-width: 600px;
            width: 100%;
            box-shadow: 0 0 40px rgba(88, 166, 255, 0.08);
        }}
        .label {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.7rem;
            color: #8b949e;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin-bottom: 1rem;
        }}
        .greeting {{
            font-size: 1.5rem;
            font-weight: 600;
            color: #e6edf3;
            word-break: break-all;
            line-height: 1.6;
            margin-bottom: 1.5rem;
        }}
        .output-box {{
            background: #0d1117;
            border: 1px solid #30363d;
            border-radius: 6px;
            padding: 1rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            color: #3fb950;
            word-break: break-all;
            margin-bottom: 1.5rem;
            min-height: 3rem;
        }}
        a {{
            color: #58a6ff;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
            text-decoration: none;
        }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <div class="card">
        <div class="label">// greeting output</div>
        <div class="greeting">Hello, {name}!</div>
        <div class="label">// rendered value</div>
        <div class="output-box">{name}</div>
        <a href="/">← Generate lagi</a>
    </div>
</body>
</html>
"""
    return render_template_string(template)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
