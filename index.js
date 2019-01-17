const {app, BrowserWindow} = require('electron');
const {PythonShell} = require('python-shell');

function createWindow() {
    window = new BrowserWindow({width: 800, height: 600});
    window.loadFile('index.html');
}

app.on('ready', createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin')
        app.quit();
})

var options = {
    args: ['test1s.docx']
};

PythonShell.run('doc-analyser.py', options, function(err, results) {
    if (err)
        throw err;
    results.forEach(function(result) {
        if (result === 'success')
            window.loadFile('results.html');
    });
});