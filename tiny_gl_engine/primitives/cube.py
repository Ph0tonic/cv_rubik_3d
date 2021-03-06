#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""cube.py: Represent a rubik's cube """

__author__ = "Lucas Bulloni, Malik Fleury, Bastien Wermeille"
__version__ = "1.0.0"

import struct
import numpy
import pyrr
import moderngl
import math


class Cube:
    def __init__(self, context, name=""):
        """ Init. """
        self.context = context
        self.name = name
        self.create_model(numpy.array([0, 0, 0]))

    def create_model(self, position):
        """ Create model matrix for transformations on the cube"""
        self.model = pyrr.matrix44.create_from_translation(position)

    def init_arrays(self):
        """ Init arrays of vertices, colors and indices """
        self.vertices = numpy.array([
            -1.0, -1.0, 1.0,    # 0
            1.0, -1.0, 1.0,     # 1
            1.0, 1.0, 1.0,      # 2
            -1.0, 1.0, 1.0,     # 3

            1.0, -1.0, 1.0,     # 4
            1.0, -1.0, -1.0,    # 5
            1.0, 1.0, -1.0,     # 6
            1.0, 1.0, 1.0,      # 7

            1.0, -1.0, -1.0,    # 8
            -1.0, -1.0, -1.0,   # 9
            -1.0, 1.0, -1.0,    # 10
            1.0, 1.0, -1.0,     # 11

            -1.0, -1.0, -1.0,   # 12
            -1.0, -1.0, 1.0,    # 13
            -1.0, 1.0, 1.0,     # 14
            -1.0, 1.0, -1.0,    # 15

            -1.0, 1.0, 1.0,     # 16
            1.0, 1.0, 1.0,      # 17
            1.0, 1.0, -1.0,     # 18
            -1.0, 1.0, -1.0,    # 19

            -1.0, -1.0, 1.0,    # 20
            1.0, -1.0, 1.0,     # 21
            1.0, -1.0, -1.0,    # 22
            -1.0, -1.0, -1.0,   # 23
        ])
        self.colors = numpy.array([
            1.0, 1.0, 1.0,
            1.0, 1.0, 1.0,
            1.0, 1.0, 1.0,
            1.0, 1.0, 1.0,

            1.0, 0.0, 0.0,
            1.0, 0.0, 0.0,
            1.0, 0.0, 0.0,
            1.0, 0.0, 0.0,

            0.0, 0.7, 0.0,
            0.0, 0.7, 0.0,
            0.0, 0.7, 0.0,
            0.0, 0.7, 0.0,

            1.0, 0.5, 0.0,
            1.0, 0.5, 0.0,
            1.0, 0.5, 0.0,
            1.0, 0.5, 0.0,

            0.0, 0.0, 1.0,
            0.0, 0.0, 1.0,
            0.0, 0.0, 1.0,
            0.0, 0.0, 1.0,

            1.0, 1.0, 0.0,
            1.0, 1.0, 0.0,
            1.0, 1.0, 0.0,
            1.0, 1.0, 0.0,
        ])
        self.indices = numpy.array([
            0, 1, 2,
            0, 2, 3,

            4, 5, 6,
            4, 6, 7,

            8, 9, 10,
            8, 10, 11,

            12, 13, 14,
            12, 14, 15,

            16, 17, 18,
            16, 18, 19,

            20, 21, 22,
            20, 22, 23,
        ])

    def init_buffers(self):
        """ Init buffers for opengl """
        # https://github.com/moderngl/moderngl/blob/master/examples/06_index_buffer.py
        context = self.context
        self.vbo = self.context.buffer(self.vertices.astype('f4').tobytes())
        self.cbo = self.context.buffer(self.colors.astype('f4').tobytes())
        self.ibo = self.context.buffer(self.indices.astype('i4').tobytes())
        vao_content = [
            (self.vbo, '3f', 'aVertex'),
            (self.cbo, '3f', 'aColor')
        ]
        self.vao = self.context.vertex_array(self.prog, vao_content, self.ibo)

    def apply_model(self):
        """ Apply the model matrix to the shaders """
        self.prog['uMMatrix'].value = tuple(self.model.flatten())

    def rotate(self, axis, clockwise):
        """ Execute rotation """
        model = self.model
        rotation_sign = 1
        if clockwise:
            rotation_sign = -1
        rotation_matrix = pyrr.matrix44.create_from_axis_rotation(
            axis, rotation_sign * math.pi/2)  # Right hand rule => 90 COUNTER CLOCKWISE !
        self.model = pyrr.matrix44.multiply(self.model, rotation_matrix)

    def __str__(self):
        """ Debug purpose"""
        return self.name

    def _repr__(self):
        """ Debug purpose"""
        self.__str__()

    # -----------------------------------------------
    # Main methods to call inside the main program

    def setup_shader(self, prog):
        """ Set the shader and apply the model matrix to it """
        self.prog = prog
        self.apply_model()

    def create_geometry(self):
        """ Create the cube """
        self.init_arrays()
        self.init_buffers()

    def render(self):
        """ Render the cube """
        self.vao.render(moderngl.TRIANGLES)
