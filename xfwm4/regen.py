#!/usr/bin/python3
bevel = 3
flat = 8
border_width = 2 + bevel + flat
tflat = 25

empty = ' '
active_color_2 = 'a'
active_hilight_2 = 'b'
active_shadow_2 = 'c'
active_color_1 = 'd'
active_hilight_1 = 'e'
active_shadow_1 = 'f'
inactive_color_2 = 'g'
inactive_hilight_2 = 'h'
inactive_shadow_2 = 'i'
inactive_color_1 = 'j'
inactive_hilight_1 = 'k'
inactive_shadow_1 = 'l'

def write_xpm(name, contents):
    fname = f'{name}.xpm'
    cname = name.replace('-', '_')
    with open(fname, 'w') as f:
        print(f'''/* XPM */
static char * {cname}[] = {{
  "{len(contents[0])} {len(contents)} 16 1",
  "  c None",
  "a c #aaaaaa s active_color_2",
  "b c #cccccc s active_hilight_2",
  "c c #888888 s active_shadow_2",
  "# c #888888 s active_mid_2",
  "x c #ffffff s active_text_color"
  "y c #888888 s inactive_text_color"
  "d c #00ff88 s active_color_1",
  "e c #44ffbb s active_hilight_1",
  "f c #00cc44 s active_shadow_1",
  "g c #aaaaaa s inactive_color_2",
  "h c #cccccc s inactive_hilight_2",
  "i c #888888 s inactive_shadow_2",
  "j c #cccccc s inactive_color_1",
  "k c #eeeeee s inactive_hilight_1",
  "l c #aaaaaa s inactive_shadow_1",''', file=f)
        for line in contents:
            print(f'  "{line}",', file=f)
        print('};', file=f)

def swap(arr, old, new):
    arr2 = []
    for l in arr:
        l = l.replace(old, new)
        arr2.append(l)
    return arr2
        
def write_border(name, contents):
    write_xpm(name + '-active', contents)
    contents = swap(contents, active_color_1, inactive_color_2)
    contents = swap(contents, active_hilight_1, inactive_hilight_2)
    contents = swap(contents, active_shadow_1, inactive_shadow_2)
    contents = swap(contents, active_color_2, inactive_color_2)
    contents = swap(contents, active_hilight_2, inactive_hilight_2)
    contents = swap(contents, active_shadow_2, inactive_shadow_2)
    write_xpm(name + '-inactive', contents)

def set(arr, x, y, color):
    l = list(arr[y])
    l[x] = color
    arr[y] = ''.join(l)

def dot(x, y, color):
    global canvas
    set(canvas, x, y, color)
    
canvas = []
brush = empty
def rect(x, y, w, h):
    global canvas
    if w < 0:
        x += w
        w = -w
    if h < 0:
        y += h
        h = -h
    for i in range(w):
        if x + i < 0 or x + i >= len(canvas[0]): continue
        for j in range(h):
            if y + j < 0 or y + j >= len(canvas): continue
            dot(x+i, y+j, brush)

def hline(x, y, w):
    rect(x, y, w, 1)

def vline(x, y, h):
    rect(x, y, 1, h)

cursor = (0,0)
def move(x, y):
    global cursor
    cursor = (cursor[0] + x, cursor[1] + y)

def draw_hline(w):
    global cursor
    hline(cursor[0], cursor[1], w)
    move(w, 0)
    
def draw_vline(h):
    global cursor
    vline(cursor[0], cursor[1], h)
    move(0, h)

def hgroove(w):
    global brush
    brush = light
    draw_hline(w)
    move(0,-1)
    brush = shadow
    draw_hline(-w)
    move(w, 1)

def vgroove(h):
    global brush
    brush = light
    draw_vline(h)
    move(-1, 0)
    brush = shadow
    draw_vline(-h)
    move(1, h)

light = active_hilight_2
main = active_color_2
shadow = active_shadow_2
tlight = active_hilight_1
tmain = active_color_1
tshadow = active_shadow_1

def blit(dst, src, x, y):
    for iy in range(len(src)):
        row = src[iy]
        for ix in range(len(row)):
            if row[ix] == ' ': continue
            set(dst, x + ix, y + iy, row[ix])

def button(name, icon):
    global canvas
    global brush
    A = 2 + bevel + tflat
    canvas = [main * A] * A
    brush = light
    rect(0, 0, A, bevel)
    vline(0, 3, tflat)
    brush = shadow
    hline(0, A-2, A)
    vline(A-1, bevel, tflat)
    brush = light
    hline(0, A-1, A)
    x = (A - len(icon[0])) // 2 + 1
    y = (A - len(icon)) // 2 + 1
    blit(canvas, icon, x, y)
    write_xpm(name + '-active', canvas)
    inactive = canvas
    inactive = swap(inactive, active_color_2, inactive_color_2)
    inactive = swap(inactive, active_hilight_2, inactive_hilight_2)
    inactive = swap(inactive, active_shadow_2, inactive_shadow_2)
    iicon = swap(icon, active_shadow_2, inactive_color_2)
    iicon = swap(iicon, '#', inactive_color_2)
    blit(inactive, iicon, x, y)
    inactive = swap(inactive, 'x', 'y')
    write_xpm(name + '-inactive', inactive)
    old_canvas = canvas
    canvas = swap(canvas, active_color_2, inactive_color_1)
    canvas = swap(canvas, active_hilight_2, inactive_hilight_1)
    canvas = swap(canvas, active_shadow_2, inactive_shadow_1)
    brush = light
    hline(0, A-1, A)
    write_xpm(name + '-prelight', canvas)
    canvas = [inactive_color_1 * A] * A
    blit(canvas, icon, x, y)
    canvas = swap(canvas, active_color_2, inactive_color_1)
    canvas = swap(canvas, active_hilight_2, inactive_hilight_1)
    canvas = swap(canvas, active_shadow_2, inactive_shadow_1)
    brush = light
    hline(0, A-1, A)
    write_xpm(name + '-pressed', canvas)
    

close = [
    '    #     #    ',
    '   #c#   #c#   ',
    '  #cxc# #cxc#  ',
    ' #cxxxc#cxxxc# ',
    '#cxxxxxcxxxxxc#',
    ' #cxxxxxxxxxc# ',
    '  #cxxxxxxxc#  ',
    '   #cxxxxxc#   ',
    '  #cxxxxxxxc#  ',
    ' #cxxxxxxxxxc# ',
    '#cxxxxxcxxxxxc#',
    ' #cxxxc#cxxxc# ',
    '  #cxc# #cxc#  ',
    '   #c#   #c#   ',
    '    #     #    ']

button('close', close)

maximize = [
"cccccccccccccc",
"cxxxxxxxxxxxxc",
"cxxxxxxxxxxxxc",
"cxxxxxxxxxxxxc",
"cxccccccccccxc",
"cxc        cxc",
"cxc        cxc",
"cxc        cxc",
"cxc        cxc",
"cxc        cxc",
"cxccccccccccxc",
"cxxxxxxxxxxxxc",
"cccccccccccccc"]

button('maximize', maximize)

hide = [
"           ",
"           ",
"           ",
"           ",
"           ",
"           ",
"           ",
"           ",
"ccccccccccc",
"cxxxxxxxxxc",
"cxxxxxxxxxc",
"cxxxxxxxxxc",
"ccccccccccc"]

button('hide', hide)

maximize_toggled = [
"    cccccccc",
"    cxxxxxxc",
"    cxxxxxxc",
"    cxccccxc",
"cccccccc cxc",
"cxxxxxxcccxc",
"cxxxxxxcxxxc",
"cxccccxccccc",
"cxc  cxc    ",
"cxccccxc    ",
"cxxxxxxc    ",
"cccccccc    "]

button('maximize-toggled', maximize_toggled)

stick = [
    " ccccccc ",
    " cxxxxxc ",
    " ccxxxcc ",
    "  cxxxc  ",
    "  cxxxc  ",
    "cccxxxccc",
    "cxxxxxxxc",
    "ccccxcccc",
    "   cxc   ",
    "   cxc   ",
    "   cxc   ",
    "   ccc   ",
]

button('stick', stick)

stick_toggled = [
    "cccccc ccc     ",
    "cxxxxc cxc  ccc",
    "cxxxxc cxccccxc",
    "cxxcccccxxxxxxc",
    "cxxcxxxxxxxxxxc",
    "cxxcccccxxxxxxc",
    "cxxxxc cxccccxc",
    "cxxxxc cxc  ccc",
    "cccccc ccc     "
]

button('stick-toggled', stick_toggled)

button('shade', [
    "    #c#    ",
    "   #cxc#   ",
    "  #cxxxc#  ",
    " #cxxxxxc# ",
    "#cxxxxxxxc#",
    "cxxxxxxxxxc",
    "ccccccccccc",
    "cxxxxxxxxxc",
    "ccccccccccc",
    ])

button('shade-toggled', [
    "ccccccccccc",
    "cxxxxxxxxxc",
    "ccccccccccc",
    "cxxxxxxxxxc",
    "#cxxxxxxxc#",
    " #cxxxxxc# ",
    "  #cxxxc#  ",
    "   #cxc#   ",
    "    #c#    ",
    ])

button('menu', [' '])

# Bottom
write_border('bottom', [shadow, light] + [main] * flat + [shadow] * bevel)

# Right
write_border('right', [shadow + light + main * flat + shadow * bevel])

# Left
write_border('left', [light * bevel + main * flat + shadow + light])

write_border('title-2', [tlight] * bevel + [tlight] * tflat + [tshadow, light])
write_border('title-3', [tlight] * bevel + [tmain] * tflat + [tshadow, light])
write_border('title-4', [tlight] * bevel + [tshadow] * tflat + [tshadow, light])

# Bottom Right
A = border_width
canvas = [main * A * 2] * A * 2
brush = empty
rect(0, 0, A, A)
cursor = (0, A+1)
hgroove(A+1)
vgroove(-A-1)
dot(A+1, A+1, light)
cursor = (A+2, 1)
hgroove(flat)
cursor = (1, A+2)
vgroove(flat)
brush = shadow
rect(A * 2 - bevel, 0, bevel, A * 2)
rect(0, A * 2 - bevel, A * 2, bevel)
write_border('bottom-right', canvas)

# Bottom Left
canvas = [main * A * 2] * A * 2
brush = empty
rect(A, 0, A, A)
cursor = (A*2, A+1)
hgroove(-A-1)
vgroove(-A-1)
dot(A-2, A+1, shadow)
cursor = (A-2, 1)
hgroove(-flat)
cursor = (2*A-1, A+2)
vgroove(flat)
brush = shadow
rect(0, A * 2 - bevel, A * 2, bevel)
brush = light
vline(0, 0, A*2)
vline(1, 0, A*2 - 1)
vline(2, 0, A*2 - 2)

write_border('bottom-left', canvas)
