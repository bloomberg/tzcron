#!/usr/bin/env python
# -*- coding: utf-8 -*-
from livereload import Server, shell

server = Server()
server.watch('*.rst', shell('make html'))
server.serve(root='_build/html')
