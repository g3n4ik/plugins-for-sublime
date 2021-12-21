import sublime, sublime_plugin
from urllib import request, parse
import os
import urllib

def f(x):
    ans = """<head>
<style>
a:link {
    color: white;
    background-color: #363636;
    text-decoration: none;
}
a:visited {
    color: white;
    background-color: #363636;
}
a:hover {
    color: white;
    background-color: #757575;
    text-decoration: underline;
}
</style>
</head><body>"""
    x = x.split('\n')
    for i in range(len(x)):
        ans = ans + "<div> <a href = '" + x[i] + "'" + ">" + x[i] + "</a> </div>"
    ans += "</body>"
    return ans
'''
class NameCommand(sublime_plugin.WindowCommand):
    def run(self, edit):
        return window.view.file_name()'''
class ExampleCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        context = self.view.substr(sublime.Region(0, self.view.size()))
        if (len(context) == 0):
            return
        address = self.view.file_name()
        data = {'context' : context, 'address' : address}
        data = parse.urlencode(data).encode()
        reg = request.Request("http://localhost:5342/", data=data)
        page = urllib.request.urlopen(reg)
        content = f(page.read().decode())
        if (len(content) == 0):
            return
        self.view.show_popup(content, flags=sublime.HTML, location=-1, max_width=400, on_navigate=self.on_choice_symbol)

    def on_choice_symbol(self, symbol):
        self.view.run_command("insert", {"characters": symbol})
        self.view.hide_popup()
