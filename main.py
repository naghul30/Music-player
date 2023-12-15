from flask import Flask, render_template, request
import pygame.mixer as mixer
import os

app = Flask(__name__)

# Initializing the mixer
mixer.init()

# Play, Stop, Load, Pause & Resume functions
def play_song(selected_song):
    try:
        mixer.music.load(selected_song)
        mixer.music.play()
        return render_template('web_music_player.html')
    except pygame.error as e:
        return f"Error: {e}"

def stop_song():
    mixer.music.stop()
    return render_template('web_music_player.html')

def load(directory):
    if directory:
        os.chdir(directory)

        tracks = [track for track in os.listdir() if track.endswith(('.mp3', '.wav'))]

        if tracks:
            return tracks
        else:
            return ['No valid audio files found in the directory.']

def pause_song():
    mixer.music.pause()
    return render_template('web_music_player.html')

def resume_song():
    mixer.music.unpause()
    return render_template('web_music_player.html')

@app.route('/')
def web_music_player():
    return render_template('web_music_player.html', tracks=[])

@app.route('/play', methods=['POST'])
def play():
    selected_song = request.form['selected_song']
    status = play_song(selected_song)
    return status

@app.route('/stop', methods=['POST'])
def stop():
    status = stop_song()
    return status

@app.route('/load', methods=['POST'])
def load_directory():
    if request.method == 'POST':
        directory = request.form['directory']
        tracks = load(directory)
        return render_template('web_music_player.html', tracks=tracks)

    # Handle GET request (initial rendering)
    return render_template('web_music_player.html', tracks=[])

@app.route('/pause', methods=['POST'])
def pause():
    status = pause_song()
    return status
    

@app.route('/resume', methods=['POST'])
def resume():
    status = resume_song()
    return status

if __name__ == '__main__':
    app.run(debug=True)
