from flask import Flask, send_file, after_this_request

app = Flask(__name__)


data = 0

def save(byte_save):
    global data
    data += byte_save
    print(f"bytes send {format_size(data)}")




@app.route('/')
def res():
    filename = 'gay.txt'
    byte_count = 0

    with open(filename, "r") as f:
     Getlen = len(f.read())
     save(Getlen)
     return f.read()




def format_size(size):
    power = 2**10
    n = 0
    labels = {0: 'B', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}
    while size > power:
        size /= power
        n += 1
    return f'{size:.2f} {labels[n]}'


if __name__ == '__main__':
    app.run()
