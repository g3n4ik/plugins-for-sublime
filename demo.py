import sublime, sublime_plugin
from urllib import request, parse
import os
import urllib

def f(x):
    ans = ""
    x = x.split('\n')
    for i in range(len(x)):
        ans = ans + "<div> <a href = '" + x[i] + "'" + ">" + x[i] + "</a> </div>"
    ans += "</body>"
    return ans


class ExampleCommand(sublime_plugin.TextCommand):
    content = ""
    def run(self, edit):
        for region in self.view.sel():
            context = self.view.substr(sublime.Region(0, region.begin()))
            if (len(context) == 0):
                return
            address = self.view.file_name()
            data = {'context' : context, 'address' : address}
            data = parse.urlencode(data).encode()
            reg = request.Request("http://localhost:5342/", data=data)
            page = urllib.request.urlopen(reg)
            content = f(page.read().decode())
            self.content = page.read().decode().split('\n')
            if (len(self.content) == 0):
                return
            self.view.show_popup_menu(self.content, on_select=self.on_choice_symbol)

    def on_choice_symbol(self, symbol):
        self.view.run_command("insert", {"characters": self.content[symbol]})
        self.view.hide_popup()