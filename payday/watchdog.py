# -*- coding: utf-8 -*-

import os

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class TemplateModifiedHandler(FileSystemEventHandler):

    def __init__(self, template_path, template_filename, template_data, render_method):
        self.template_path = template_path
        self.template_filename = template_filename
        self.template_data = template_data
        self.render_method = render_method

    def on_modified(self, event):
        # print event.src_path
        if event.src_path == os.path.join(self.template_path, self.template_filename):
            print("template was modified")
            self.render_method(
                self.template_filename, self.template_data)
