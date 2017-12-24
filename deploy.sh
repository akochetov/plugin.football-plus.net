DIR="/home/pi/.kodi/addons/plugin.football-plus.net/"
if [ ! -d "$DIR" ]
then
 mkdir "$DIR"
 mkdir "$DIR/resources/"
fi
cp fp.py "$DIR"
cp icon.png "$DIR"
cp default.py "$DIR"
cp addon.xml "$DIR"
cp resources/settings.xml "$DIR/resources"
