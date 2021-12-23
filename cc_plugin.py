import os
import urllib
from urllib import request, parse

import sublime, sublime_plugin


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
            self.content = page.read().decode().split('\n')
            if (len(self.content) == 0):
                return
            self.view.show_popup_menu(self.content, on_select=self.on_choice_symbol)

    def on_choice_symbol(self, symbol):
        if(symbol == -1):
            self.view.hide_popup()
            return
        self.view.run_command("insert", {"characters": self.content[symbol]})
        self.view.hide_popup()
