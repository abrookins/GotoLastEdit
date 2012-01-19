import sublime, sublime_plugin


LAST_EDITS_SETTING = 'last_edits'


class RecordLastEdit(sublime_plugin.EventListener):
    def on_modified(self, view):
        last_edits = view.settings().get(LAST_EDITS_SETTING, {}) 
        edit_position = view.sel()[0] 
        last_edits[str(view.id())] = {'a': edit_position.a, 'b': edit_position.b}
        view.settings().set(LAST_EDITS_SETTING, last_edits) 

 
class GotoLastEdit(sublime_plugin.TextCommand): 
    # The position the cursor was at before the command fired. Saved when the
    # command is run, so that if the user runs the command again before making
    # another edit in the file, the cursor returns to its original position.
    original_position = None

    def move_cursor_to_region(self, region):
        """ Clear the cursor's position and move it to `region`. """
        cursor = self.view.sel()
        self.original_position = cursor[0] 
        cursor.clear()
        cursor.add(region)
        self.view.show(region) 

    def run(self, edit): 
        """
        If there was a last edit recorded for the view, store the current
        position as self.original_position and move the cursor to the position
        of the last edit.

        If the cursor is currently at the same position as the last edit, and
        there `self.original_position` is available, then return the cursor to
        its original position.
        """ 
        last_edits = self.view.settings().get(LAST_EDITS_SETTING, {})
        last_edit = last_edits.get(str(self.view.id()), None)
        current_position = self.view.sel()[0]

        if last_edit is None:
            return

        last_edit_region = sublime.Region(
            long(last_edit['a']), long(last_edit['b']))

        if self.original_position is not None \
            and current_position == last_edit_region:
            self.move_cursor_to_region(self.original_position)
            return

        self.move_cursor_to_region(last_edit_region)
