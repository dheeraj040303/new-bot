echo "Cloning Repo...."
git clone https://github.com/dheerajdalbanjan/movie_bot.git /movie_bot
cd /movie_bot
pip3 install -r requirements.txt
echo "Starting Bot...."
python3 api/main.py