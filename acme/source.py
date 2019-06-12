#!/usr/bin/env python
import numpy as np
import cairo

WIDTH, HEIGHT = 2**11, 2**11

np.random.seed(124389339)
REV = 7
POLY = 5
NOISE_AMP = 0.3
SIZE = 0.01
GROWTH = 0.025
NUM_DIV = 2**7
LINE_WIDTH = 0.0005

surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
ctx = cairo.Context(surface)

ctx.scale(WIDTH, HEIGHT)

ctx.rectangle(0, 0, 1, 1)
ctx.set_source_rgb(0, 0, 0)
ctx.fill()

ctx.rectangle(0.3, 0, 0.1, 1)
ctx.rectangle(0.45, 0, 0.1, 1)
ctx.rectangle(0.6, 0, 0.1, 1)
ctx.set_source_rgba(1, 1, 1, 0.25)
ctx.fill()

ctx.translate(0.5, 0.1)
ctx.set_source_rgb(1,0,0)
ctx.set_line_width(LINE_WIDTH)

def weave(x1i, y1i, x1f, y1f, x2i, y2i, x2f, y2f, div):
    l1x = np.linspace(x1i, x1f, div)
    l1y = np.linspace(y1i, y1f, div)
    l2x = np.linspace(x2i, x2f, div)
    l2y = np.linspace(y2i, y2f, div)
    for i in range(div):
        ctx.line_to(l1x[i],l1y[i])
        ctx.line_to(l2x[i],l2y[i])
        ctx.stroke()

theta = np.linspace(0, REV*2*np.pi, REV*POLY)
theta += np.random.randn(len(theta)) * NOISE_AMP
x = SIZE *theta * np.cos(theta)
y = SIZE *theta * np.sin(theta) +  GROWTH * theta
for i in range(len(theta)-2):
    weave(x[i],y[i],x[i+1],y[i+1], x[i+1],y[i+1],x[i+2],y[i+2], div=NUM_DIV)

surface.write_to_png("image.png")
