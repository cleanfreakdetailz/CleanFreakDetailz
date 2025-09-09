from flask import Flask, render_template
import os

app = Flask(__name__)


@app.route('/')
def home():
    # Get list of images in the Work folder
    work_images = []
    work_dir = os.path.join(app.static_folder, 'Work')

    if os.path.exists(work_dir):
        for filename in os.listdir(work_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                # Check if filename follows the "WorkX" pattern
                if filename.startswith('Work'):
                    try:
                        # Extract the number from the filename
                        num_part = filename[4:].split('.')[0]  # Remove "Work" prefix and extension
                        number = int(num_part)
                        work_images.append({
                            'filename': f"Work/{filename}",
                            'number': number
                        })
                    except ValueError:
                        # If it doesn't follow the pattern, just add it
                        work_images.append({
                            'filename': f"Work/{filename}",
                            'number': 0  # Default value for sorting
                        })

    # Sort by number if possible
    work_images.sort(key=lambda x: x['number'])

    return render_template('home.html', title='Home', work_images=work_images)


@app.route('/contact')
def contact():
    return render_template('contactme.html')


@app.route('/services')
def services():
    return render_template('services.html', title='Our Services')


@app.route('/extraservices')
def extraservices():
    return render_template('extraservices.html', title='Extra Services')


@app.route('/packages')
def packages():
    return render_template('packages.html', title='Service Packages')


if __name__ == '__main__':
    app.run(debug=True)