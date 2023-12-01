from manim import *
import math
import os

class BraceAnnotation(Scene):
    def construct(self):
        dot = Dot((-2,-1,0))
        dot2 = Dot((2,1,0))
        line = Line(dot.get_center(),dot2.get_center()).set_color(color=ORANGE)
        b1 = Brace(line)
        b1text = b1.get_text("Horizontal distance")
        b2 = Brace(line,direction = line.copy().rotate(PI/2).get_unit_vector())
        b2text = b2.get_tex("x-x_1")
        self.add(line,dot,dot2,b2,b2text,b1,b1text)


class GradientImageFromArray(Scene):
    def construct(self):
        n = 1024
        imageArray = np.uint8(
            [[256 * np.sin(i*PI/256) for i in range(0, n)] for j in range(0, n)]
        )
        image = ImageMobject(imageArray).scale(2)
        image.background_rectangle = SurroundingRectangle(image, GREEN)
        self.add(image, image.background_rectangle)

class ShowGraph(Scene): 
    def construct(self): 
        print("dot = Dot()")
        dot = Dot()
        self.wait(2)

        print("dot.to_edge(UL)")
        dot.to_edge(UL)
        self.play(FadeIn(dot))
        self.wait(2)

        print("text = TextMobject(\"text\")")
        text = Text("text")
        self.wait(2)

        print("text.to_corner(UP)")
        text.to_corner(UP)
        self.play(Write(text))
        self.wait(2)
class testGraph(Scene):
    def construct(self):
        axes = Axes(
                x_range = [0, 10, 1],
                y_range = [-2, 10, 1],
                x_length = 10,
                axis_config = {
                    "color":GREEN,
                }
            ) 
        def func(x):
            N = 100
            result = N**x
            for k in range(N):
                k += 1
                result *= k/(x+k)
            return result
        def factorial(x):
            x = int(x)
            result = 1
            for k in range(x):
                k += 1
                result *= k 
            return result
        def test(x):
            if x != 0:
                return 1/x
            return 0
        func_graph = axes.plot(func,color = RED)
        fac_graph = axes.plot(factorial,color = BLUE)
        test_graph = axes.plot(test,color = ORANGE)
        group = VGroup(axes,func_graph,fac_graph,test_graph)
        # self.play(Create(group))
        self.add(group)
class imageScene(Scene):
    def construct(self):
        image = ImageMobject(np.uint8([[0, 100, 30, 200],[255, 0, 5, 33]]))
        image.height = 7
        self.add(image)

class mandelbrotScene(Scene):
    def calc_steps(self,C:complex,max_step:int = 255):
        Z = complex(0,0)
        step = 0
        while abs(Z) <= 2 and step < max_step:
            Z = Z ** 2 + C
            step+=1
        return step/max_step*255
    def get_mandelbrot_grid(self,COL:int,RAW:int,xbase:float,ybase:float,xscale:float,yscale:float,max_step=255):
        grid = [[self.calc_steps(complex(xbase+(1/xscale)*(col/COL*4-2),ybase+(1/yscale)*-1*(raw/RAW*4-2)),max_step) for col in range(COL)] for raw in range(RAW)] 
        return grid

    def get_mandelbrot(self):
        time = self.time.get_value()
        grid = self.get_mandelbrot_grid(self.COL,self.RAW,self.xbase,self.ybase,self.xscale ** time,self.yscale ** time,self.max_step)
        res = ImageMobject(np.uint8(grid))
        res.height = 7
        return res


    def construct(self):
        self.COL = 512
        self.RAW = 512
        self.xscale = 1.1
        self.yscale = 1.1
        self.xbase = -0.861146993077
        self.ybase = -0.2349923738865
        self.max_step = 255
        self.time = ValueTracker(0)
        image = always_redraw(self.get_mandelbrot)
        
        self.add(SurroundingRectangle(image,GREEN))
        self.add(image)
        self.play(self.time.animate(run_time=100,rate_func=smooth).set_value(1000))
