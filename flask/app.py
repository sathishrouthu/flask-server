from flask import Flask, jsonify, request, render_template_string
import os

app = Flask(__name__)

# A simple in-memory structure to store tasks
tasks = []

@app.route('/', methods=['GET'])
def home():
    # Display existing tasks and a form to add a new task
    html = '''
<!DOCTYPE html>
<html>
<head>
    <title>Todo List</title>
</head>
<body>
    <h1>Todo List</h1>
    <form action="/add" method="POST">
        <input type="text" name="task" placeholder="Enter a new task">
        <input type="submit" value="Add Task">
    </form>
    <ul>
        {% for task in tasks %}
        <li>{{ task }} <a href="/delete/{{ loop.index0 }}">x</a></li>
        {% endfor %}
    </ul>
</body>
</html>
'''
    return render_template_string(html, tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    # Add a new task from the form data
    task = request.form.get('task')
    if task:
        tasks.append(task)
    return home()

@app.route('/delete/<int:index>', methods=['GET'])
def delete_task(index):
    # Delete a task based on its index
    if index < len(tasks):
        tasks.pop(index)
    return home()

@app.route('/get/images/list', methods=['GET'])
def get_images_list():
    # Directory where images are stored, relative to the app.py file
    image_dir = 'images'
    
    # Check if the directory exists
    if not os.path.isdir(image_dir):
        return jsonify({"error": f"'{image_dir}' directory not found."}), 404

    # List of allowed image extensions
    allowed_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'}

    try:
        # List all files in the directory and filter for images
        image_names = [f for f in os.listdir(image_dir) 
                       if os.path.isfile(os.path.join(image_dir, f)) and os.path.splitext(f)[1].lower() in allowed_extensions]
        return jsonify(image_names)
    except Exception as e:
        return jsonify({"error": "An error occurred while reading the directory.", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
