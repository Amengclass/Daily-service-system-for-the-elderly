from flask import Flask, render_template

app = Flask(__name__)


@app.route('/music')
def music():
    return render_template('music.html')


# 获取音乐列表
def get_song_list():
    songs = []
    for filename in os.listdir(MUSIC_DIRECTORY):
        if filename.endswith('.mp3'):
            songs.append(filename)
    return songs


# 获取音乐文件路径
def get_song_path(song_name):
    return os.path.join(MUSIC_DIRECTORY, song_name)


# 获取音乐文件
@app.route('/play_song')
def play_song():
    song_name = request.args.get('song')
    # song_path = get_song_path(song_name)
    return send_from_directory(MUSIC_DIRECTORY, song_name)


# 获取音乐列表
@app.route('/get_songs')
def get_songs():
    songs = get_song_list()


if __name__ == '__main__':
    app.run(debug=True)
