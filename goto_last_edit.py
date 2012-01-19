import sublime_plugin


# the last edited Region, keyed to View.id
_last_edits = {}


class RecordLastEdit(sublime_plugin.EventListener):
    def on_modified(self, view):
        _last_edits[view.id()] = view.sel()[0]

 
class GotoLastEdit(sublime_plugin.TextCommand): 
    def run(self, edit):
        last_edit = _last_edits.get(self.view.id(), None)

        if last_edit != None:
            self.view.sel().clear()
            self.view.sel().add(last_edit)
            self.view.show(last_edit)
