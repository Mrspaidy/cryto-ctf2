from flask import Flask, render_template, request, redirect, url_for, session
import base64

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a secure random key

# Precomputed encrypted flags
ENCRYPTED_FLAGS = {
    'level1': 'Q1RGe2Jhc2U2NF9lYXN5fQ==',  # CTF{base64_easy}
    'level2': 'FWI{fdhvdu_hdvb}',          # CTF{caesar_easy} (Caesar shift: +3)
    'level3': 'EZY{lxwlzozxogf_tqln}'      # CTF{substitution_easy} (Substitution cipher)
}

# Expected flags
FLAGS = {
    'level1': 'CTF{base64_easy}',
    'level2': 'CTF{caesar_easy}',
    'level3': 'CTF{substitution_easy}'
}

@app.route('/')
def home():
    return redirect(url_for('level1'))

@app.route('/level1', methods=['GET', 'POST'])
def level1():
    if request.method == 'POST':
        user_input = request.form.get('answer', '')
        if user_input.strip() == FLAGS['level1']:
            session['passed_level1'] = True
            return redirect(url_for('level2'))
        else:
            return render_template('level1.html', encrypted=ENCRYPTED_FLAGS['level1'], error="Wrong answer!")
    return render_template('level1.html', encrypted=ENCRYPTED_FLAGS['level1'], error=None)

@app.route('/level2', methods=['GET', 'POST'])
def level2():
    if not session.get('passed_level1'):
        return redirect(url_for('level1'))
    
    if request.method == 'POST':
        user_input = request.form.get('answer', '')
        if user_input.strip() == FLAGS['level2']:
            session['passed_level2'] = True
            return redirect(url_for('level3'))
        else:
            return render_template('level2.html', encrypted=ENCRYPTED_FLAGS['level2'], error="Wrong answer!")
    return render_template('level2.html', encrypted=ENCRYPTED_FLAGS['level2'], error=None)

@app.route('/level3', methods=['GET', 'POST'])
def level3():
    if not session.get('passed_level2'):
        return redirect(url_for('level2'))
    
    if request.method == 'POST':
        user_input = request.form.get('answer', '')
        if user_input.strip() == FLAGS['level3']:
            session['passed_level3'] = True
            return redirect(url_for('success'))
        else:
            return render_template('level3.html', encrypted=ENCRYPTED_FLAGS['level3'], error="Wrong answer!")
    return render_template('level3.html', encrypted=ENCRYPTED_FLAGS['level3'], error=None)

@app.route('/success')
def success():
    if not session.get('passed_level3'):
        return redirect(url_for('level3'))
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)