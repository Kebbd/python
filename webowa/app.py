from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import matplotlib
matplotlib.use('agg')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define the association table for the many-to-many relationship
training_exercises = db.Table(
    'training_exercises',
    db.Column('training_id', db.Integer, db.ForeignKey('training.id')),
    db.Column('exercise_id', db.Integer, db.ForeignKey('exercise.id'))
)

class Training(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), nullable=False)
    exercises = db.relationship('Exercise', secondary=training_exercises, backref='training', lazy='dynamic')

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    repetitions = db.Column(db.Integer, nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    load = db.Column(db.Integer, nullable=False)
    training_id = db.Column(db.Integer, db.ForeignKey('training.id'))

    @property
    def volume(self):
        return self.repetitions * self.sets * self.load

class VolumeHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), nullable=False)
    volume = db.Column(db.Integer, nullable=False)

@app.route('/')
def index():
    trainings = Training.query.all()
    return render_template('index.html', trainings=trainings)

@app.route('/add_training', methods=['POST'])
def add_training():
    if request.method == 'POST':
        date = request.form['date']

        # Create a new training
        training = Training(date=date)
        db.session.add(training)
        db.session.commit()

        # Add exercises to the training
        exercise_names = request.form.getlist('exercise_name')
        repetitions = map(int, request.form.getlist('repetitions'))
        sets = map(int, request.form.getlist('sets'))
        loads = map(int, request.form.getlist('load'))

        for name, reps, set_count, load in zip(exercise_names, repetitions, sets, loads):
            exercise = Exercise(name=name, repetitions=reps, sets=set_count, load=load)
            training.exercises.append(exercise)
            db.session.add(exercise)

            # Add to volume history
            volume_history = VolumeHistory(date=date, volume=exercise.volume)
            db.session.add(volume_history)

        db.session.commit()
        return redirect(url_for('index'))

@app.route('/plot')
def plot():
    volume_history = VolumeHistory.query.all()

    dates = [entry.date for entry in volume_history]
    volumes = [entry.volume for entry in volume_history]

    plt.figure(figsize=(10, 5))
    plt.bar(dates, volumes, color='blue')
    plt.xlabel('Date')
    plt.ylabel('Volume')
    plt.title('Training Volume Over Time')

    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template('plot.html', plot_url=plot_url)

if __name__ == '__main__':
    app.run(debug=True)
