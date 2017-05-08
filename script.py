import mdl
from display import *
from matrix import *
from draw import *

ARG_COMMANDS = [ 'line', 'scale', 'move', 'rotate', 'save', 'circle', 'bezier', 'hermite', 'box', 'sphere', 'torus' ]

def run(filename):
    """
    This function runs an mdl script
    """
    color = [255, 255, 255]
    tmp = new_matrix()
    ident( tmp )

    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return

    ident(tmp)
    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    edges = []
    step = 0.1
    print stack
    for command in commands:

        if command[0] in ARG_COMMANDS:
            args = command[1:]

        if command[0] == 'pop':
            stack.pop()
            
        elif command[0] == 'push':
            stack.append(copy_matrix(stack[-1]))

        elif command[0] == 'move':            
            t = make_translate(float(args[0]), float(args[1]), float(args[2]))
            matrix_mult( stack[-1], t )
            stack[-1] = t

        elif command[0] == 'rotate':            
            theta = float(args[1]) * (math.pi / 180)
            
            if args[0] == 'x':
                t = make_rotX(theta)
            elif args[0] == 'y':
                t = make_rotY(theta)
            else:
                t = make_rotZ(theta)
            matrix_mult( stack[-1], t )
            stack[-1] = t

        elif command[0] == 'scale':            
            t = make_scale(float(args[0]), float(args[1]), float(args[2]))
            matrix_mult( stack[-1], t )
            stack[-1] = t

        elif command[0] == 'box':
            add_box(edges,
                    float(args[0]), float(args[1]), float(args[2]),
                    float(args[3]), float(args[4]), float(args[5]))
            matrix_mult( stack[-1], edges )
            draw_polygons(edges, screen, color)
            edges = []

        elif command[0] == 'sphere':
            add_sphere(edges,
                       float(args[0]), float(args[1]), float(args[2]),
                       float(args[3]), step)
            matrix_mult( stack[-1], edges )
            draw_polygons(edges, screen, color)
            edges = []

        elif command[0] == 'torus':
            add_torus(edges,
                      float(args[0]), float(args[1]), float(args[2]),
                      float(args[3]), float(args[4]), step)
            matrix_mult( stack[-1], edges )
            draw_polygons(edges, screen, color)
            edges = []

        elif command[0] == 'line':            
            add_edge( edges,
                      float(args[0]), float(args[1]), float(args[2]),
                      float(args[3]), float(args[4]), float(args[5]) )

        elif command[0] == 'display' or command[0] == 'save':
            if command[0] == 'display':
                display(screen)
            else:
                save_extension(screen, args[0])
            
        print command
