#!/usr/bin/env python
import numpy as np
import cairo

WIDTH, HEIGHT = 1024, 1024

SHAPE_DIV = 2**8
SHAPE_A, SHAPE_B, SHAPE_C = 7, 2, 7
SHAPE_SCALE = 0.02
SHAPE_LW = 0.0015
GEN_NUM = 2**7
ITER_AMP, ITER_NOISE, ITER_NOISE_DECAY, ITER_ALPHA_DECAY= 1.02, 0.01, 2**7, 2**5

surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
ctx = cairo.Context(surface)

ctx.scale(WIDTH, HEIGHT)

ctx.rectangle(0, 0, 1, 1)
ctx.set_source_rgb(0, 0, 0)
ctx.fill()

ctx.translate(0.5, 0.5)

theta = np.linspace(0, 2*np.pi, SHAPE_DIV)
r = (SHAPE_A+SHAPE_B*np.cos(SHAPE_C*theta))*SHAPE_SCALE
x = r * np.cos(theta)
y = r * np.sin(theta)

for gen in range(GEN_NUM):

    for i in range(len(x)):
        ctx.line_to(x[i], y[i])
    ctx.set_source_rgba(1,1,1, np.exp(-gen/ITER_ALPHA_DECAY))
    ctx.set_line_width(SHAPE_LW)
    ctx.stroke()

    x = ITER_AMP*x + ITER_NOISE*np.random.randn(len(x)) * (gen/ITER_NOISE_DECAY)
    y = ITER_AMP*y + ITER_NOISE*np.random.randn(len(y)) * (gen/ITER_NOISE_DECAY)

surface.write_to_png("image.png")
