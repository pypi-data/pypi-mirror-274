import os
import random
import inspect
from collections import OrderedDict

import System.Text

import rhinoscriptsyntax as rs

# random is used here for fuzz testing, not Cryptography.  
# But could Windows OS generated randomness be repeatable
# between instances of the same VM image, e.g. CI runners?  
# If so use:
# random.seed(time.time())
# Otherwise, assuming os.urandom includes the time already:
SEED = os.urandom(10)
random.seed(SEED)

# Extents of viewport
MIN_X, MAX_X, MIN_Y, MAX_Y = -10.0, 110.0, -10.0, 40.0

def random_boolean():
    return random.choice([True, False])

def random_number(min_ = MIN_X, max_ = MAX_X):
    return random.uniform(min_, max_)

def random_pair():
    return random_number(), random_number()

def random_triple():
    return random_pair() + (random_number(),)

def random_int(min_ = 2, max_ = 17):
    return random.randint(min_, max_)

def random_triples(n = None):
    n = n or random_int(min_ = 3)
    return tuple(random_triple() for __ in range(n))

# def random_point():

def random_nurbs_curve(length = None, degree = None):
    length = length or random_int()

    # The control points are a list of at least degree+1 points.
    # https://developer.rhino3d.com/guides/opennurbs/nurbs-geometry-overview/
    degree = degree or random_int(1, length-1)

    knots = []

    i = 0
    while len(knots) < degree + length -1:
        multiplicity = random_int(1, degree)
        knots.extend([i,] * multiplicity)
        i += 1

    #
    points = random_triples(length)

    return rs.AddNurbsCurve(points, knots, degree) 

try:
    unichr
except NameError:
    unichr = chr

def valid_unicode_codepoint_or_empty_str(i):
    if not System.Text.Rune.IsValid(i):
        return ''
        
    return System.String(System.Text.Rune(i))





def random_string(length = None):
    length = length or random_int()
    return u''.join(valid_unicode_codepoint_or_empty_str(random_int(0, 0x10FFFF)) 
                    for __ in range(length)
                   )

def random_torus(base, minor_radius, delta_radius):
    return rs.AddTorus(base, minor_radius + delta_radius, minor_radius)

OBJECT_GENERATORS = [rs.AddArc3Pt, #rs.AddBox, 
                     rs.AddCircle3Pt, 
                     rs.AddCone, rs.AddCurve, rs.AddEllipse3Pt, rs.AddLine,
                     rs.AddPoint, rs.AddPolyline,
                     rs.AddRectangle, rs.AddSphere, rs.AddSpiral, # random_torus,
                     rs.AddTextDot, random_nurbs_curve
                     ]

def needed_args(func):
    arg_spec = inspect.getargspec(func)
    if arg_spec.defaults is None:
        return arg_spec.args
    return arg_spec.args[:-len(arg_spec.defaults)]



random_funcs = OrderedDict([
                (('start', 'end', 'first', 'second', 'third', 'center'), random_triple),
                (('points','corners'), random_triples),
                (('point', ), random_triple),
                (('plane','base'), lambda : rs.WorldXYPlane()),
                (('height', 'width', 'radius', 'pitch'), random_number),
                (('turns',), random_int),
                (('text',), random_string),
                ])


def random_Geometry(gens = None):

    N = random_int(1, 14)

    gens = gens or OBJECT_GENERATORS

    Geom = []
    for __ in range(N):
        obj_gen = random.choice(gens)
        kwargs = {}
        for arg in needed_args(obj_gen):
            names_and_random_funcs = ((name, v) 
                                    for k, v in random_funcs.items()
                                    for name in k)
            for name, random_func in names_and_random_funcs:
                if name in arg:
                    kwargs[arg] = random_func()
                    break
                #
            else: # no break in inner most for loop - no name found
                raise KeyError('No random func found for arg: %s' % arg)
        try:
            geom = obj_gen(**kwargs)        
        except Exception:
            print('Error generating: %s geom from: %s ' % (obj_gen.__name__, kwargs))
            continue
        if geom:
            Geom.append(str(geom))
    
    return Geom