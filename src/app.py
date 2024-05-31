from flask import Flask, render_template, send_from_directory, url_for, request
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed 
from wtforms import SubmitField
import getdepth

def cleardir(dirpath):
    import os, shutil
    folder = dirpath
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'osadjapso'
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

class UploadForm(FlaskForm):
    photo = FileField(
        validators=[
            FileAllowed(photos, 'Only images are allowed'),
            FileRequired('File required')
        ]
    )
    submit = SubmitField('Upload')

@app.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)

@app.route('/', methods=['GET','POST'])
def upload_image():

    cleardir("uploads/")
    form = UploadForm()
    if form.validate_on_submit():
        input_img = form.photo.data
        filename = photos.save(input_img)        
        file_url = url_for('get_file', filename=getdepth.GetDepth('uploads/'+filename))
    else:
        file_url = None
    return render_template('index.html', form=form, file_url=file_url)