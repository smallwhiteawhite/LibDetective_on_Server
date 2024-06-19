from flask import Flask, request, send_file, render_template
import os
from LibDetectiveRepo import LibDetective



app = Flask(__name__)

repo_folder = os.path.join(os.path.dirname(__file__), 'LibDetectiveRepo')


@app.route('/')
def index():
    message = request.args.get('message', '')
    return render_template('index.html', message=message)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return '没有文件上传'

    file = request.files['file']

    if file.filename == '':
        return '没有选择文件'

    # 如果文件存在
    if file:
        # 检查文件后缀名是否为.zip
        if not file.filename.endswith('.zip'):
            return '<script>alert("请上传后缀名为.zip的压缩包");window.location.href="/";</script>'
        file_path = os.path.join(repo_folder, file.filename)
        file.save(file_path)
        LibDetective.detect_libraries(file_path)

        prefix = file.filename.replace(".zip", "")
        return send_file(prefix + "_result.txt", as_attachment=True)

    return '文件上传失败'


if __name__ == '__main__':
    app.run(debug=True)
