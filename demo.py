import sublime, sublime_plugin


def f(x):
    ans = ''
    x = x.split('\n')
    for i in range(len(x)):
        ans += '<div><a href = ' + str(x[i]) + '>' + str(x[i]) + '</a> </div>'
    return ans


class ExampleCommand(sublime_plugin.TextCommand):
    def run(self, edit):    
        context = self.view.substr(sublime.Region(0, self.view.size()))       
        print(context)
        content = f('aaaa\n vvvv')
        print(content)
        self.view.show_popup(content, flags=sublime.HTML, location=-1, max_width=400, on_navigate=self.on_choice_symbol)

    def on_choice_symbol(self, symbol):
        self.view.run_command("insert", {"characters": symbol})
        self.view.hide_popup()
