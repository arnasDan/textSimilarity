from infi.systray import SysTrayIcon
import webbrowser
import flask_server

def open_about(systray):
    webbrowser.open('https://github.com/arnasDan/textSimilarity')
def on_quit_callback(systray):
    exit(0)
menu_options = (
    ('About', None, open_about),
)
systray = SysTrayIcon('icon.ico', 'Text search for Word', menu_options, on_quit=on_quit_callback)
systray.start()

flask_server.run_server()