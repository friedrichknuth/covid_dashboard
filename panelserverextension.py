from subprocess import Popen

def load_jupyter_server_extension(nbapp):
    """serve the notebook panel app with bokeh server"""
    Popen(["panel", "serve", "dashboard-panel.ipynb", "--allow-websocket-origin=*"])