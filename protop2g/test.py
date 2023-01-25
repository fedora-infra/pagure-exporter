#!/usr/bin/env python3

from asciimatics.widgets import Frame, ListBox, Layout, Divider, Text, \
    Button, TextBox, Widget
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication
import sys
import sqlite3


class ContactModel(object):
    def __init__(self):
        # Create a database in RAM.
        self.db = sqlite3.connect(':memory:')
        self.db.row_factory = sqlite3.Row

        # Create the basic contact table.
        self.db.cursor().execute('''
            CREATE TABLE contacts(
                id INTEGER PRIMARY KEY,
                name TEXT,
                phone TEXT,
                address TEXT,
                email TEXT,
                notes TEXT)
        ''')
        self.db.commit()

        # Current contact when editing.
        self.current_id = None

    def add(self, contact):
        self.db.cursor().execute('''
            INSERT INTO contacts(name, phone, address, email, notes)
            VALUES(:name, :phone, :address, :email, :notes)''',
                                  contact)
        self.db.commit()

    def get_summary(self):
        return self.db.cursor().execute(
            "SELECT name, id from contacts").fetchall()

    def get_contact(self, contact_id):
        return self.db.cursor().execute(
            "SELECT * from contacts WHERE id=:id", {"id": contact_id}).fetchone()

    def get_current_contact(self):
        if self.current_id is None:
            return {"name": "", "address": "", "phone": "", "email": "", "notes": ""}
        else:
            return self.get_contact(self.current_id)

    def update_current_contact(self, details):
        if self.current_id is None:
            self.add(details)
        else:
            self.db.cursor().execute('''
                UPDATE contacts SET name=:name, phone=:phone, address=:address,
                email=:email, notes=:notes WHERE id=:id''',
                                      details)
            self.db.commit()

    def delete_contact(self, contact_id):
        self.db.cursor().execute('''
            DELETE FROM contacts WHERE id=:id''', {"id": contact_id})
        self.db.commit()


class ListView(Frame):
    def __init__(self, screen, model):
        super(ListView, self).__init__(screen,
                                       screen.height * 2 // 3,
                                       screen.width * 2 // 3,
                                       on_load=self.reload_list,
                                       hover_focus=True,
                                       can_scroll=False,
                                       title="Contact List")
        # Save off the model that accesses the contacts database.
        self.model = model

        # Create the form for displaying the list of contacts.
        self.list_view = ListBox(
            Widget.FILL_FRAME,
            model.get_summary(),
            name="contacts",
            add_scroll_bar=True,
            on_change=self.on_pick,
            on_select=self.edit)
        self.edit_button = Button("Edit", self.edit)
        self.delete_button = Button("Delete", self.delete)
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(self.list_view)
        layout.add_widget(Divider())
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Add", self.add), 0)
        layout2.add_widget(self.edit_button, 1)
        layout2.add_widget(self.delete_button, 2)
        layout2.add_widget(Button("Quit", self.quit), 3)
        self.fix()
        self.on_pick()

    def on_pick(self):
        self.edit_button.disabled = self.list_view.value is None
        self.delete_button.disabled = self.list_view.value is None

    def reload_list(self, new_value=None):
        self.list_view.options = self.model.get_summary()
        self.list_view.value = new_value

    def add(self):
        self.model.current_id = None
        raise NextScene("Edit Contact")

    def edit(self):
        self.save()
        self.model.current_id = self.data["contacts"]
        raise NextScene("Edit Contact")

    def delete(self):
        self.save()
        self.model.delete_contact(self.data["contacts"])
        self.reload_list()

    @staticmethod
    def quit():
        raise StopApplication("User pressed quit")


class ContactView(Frame):
    def __init__(self, screen, model):
        super(ContactView, self).__init__(screen,
                                          screen.height * 2 // 3,
                                          screen.width * 2 // 3,
                                          hover_focus=True,
                                          can_scroll=False,
                                          title="Contact Details",
                                          reduce_cpu=True)
        # Save off the model that accesses the contacts database.
        self.model = model

        # Create the form for displaying the list of contacts.
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(Text("Name:", "name"))
        layout.add_widget(Text("Address:", "address"))
        layout.add_widget(Text("Phone number:", "phone"))
        layout.add_widget(Text("Email address:", "email"))
        layout.add_widget(TextBox(
            Widget.FILL_FRAME, "Notes:", "notes", as_string=True, line_wrap=True))
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("OK", self.ok), 0)
        layout2.add_widget(Button("Cancel", self.cancel), 3)
        self.fix()

    def reset(self):
        # Do standard reset to clear out form, then populate with new data.
        super(ContactView, self).reset()
        self.data = self.model.get_current_contact()

    def ok(self):
        self.save()
        self.model.update_current_contact(self.data)
        raise NextScene("Main")

    @staticmethod
    def cancel():
        raise NextScene("Main")


def demo(screen, scene):
    scenes = [
        Scene([ListView(screen, contacts)], -1, name="Main"),
        Scene([ContactView(screen, contacts)], -1, name="Edit Contact")
    ]

    screen.play(scenes, stop_on_resize=True, start_scene=scene, allow_int=True)


contacts = ContactModel()
last_scene = None

while True:
    try:
        Screen.wrapper(demo, catch_interrupt=True, arguments=[last_scene])
        sys.exit(0)
    except ResizeScreenError as e:
        last_scene = e.scene