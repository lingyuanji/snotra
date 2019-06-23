#!/usr/bin/env python
import numpy as np
import cairo

WIDTH, HEIGHT = 2**11, 2**11
NUM_PTS = 2**18
NUM_CHECKERED = 3
ABCD_INIT = [2.2, 2.3, 1.7, 1.6]
ABCD_END = [2.3, 1.9, 2.2, 1.1]
ALPHA = 0.25
ZOOM = 0.8
PT_SIZE = 0.0005

surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
ctx = cairo.Context(surface)

ctx.scale(WIDTH, HEIGHT)

ctx.rectangle(0, 0, 1, 1)
ctx.set_source_rgb(0, 0, 0)
ctx.fill()

def de_jong_ifs(a, b, c, d, num):
    def de_jong(p):
        xnew = np.sin(a * p[1]) - np.cos(b * p[0])
        ynew = np.sin(c * p[0]) - np.cos(d * p[1])
        return (xnew, ynew)
    result = [(0,0)]
    for i in range(num):
        result.append(de_jong(result[-1]))
    return np.array(result)

ctx.set_source_rgba(1,1,1,ALPHA)
ctx.set_line_width(0)
abcd_init = np.array(ABCD_INIT)
abcd_end = np.array(ABCD_END)

for i in range(NUM_CHECKERED):
    for j in range(NUM_CHECKERED):
        abcd = abcd_init + ((j+i*NUM_CHECKERED)/NUM_CHECKERED**2)*(abcd_end - abcd_init)
        result = de_jong_ifs(*abcd, NUM_PTS)/4+0.5
        shift_vec = np.array([j/NUM_CHECKERED, i/NUM_CHECKERED])
        shifted_result = (result * ZOOM + (1-ZOOM)/2) / NUM_CHECKERED + shift_vec
        for p in shifted_result:
            ctx.arc(p[0], p[1], PT_SIZE, 0, 2*np.pi)
            ctx.fill()
            ctx.stroke()

surface.write_to_png("image.png")
