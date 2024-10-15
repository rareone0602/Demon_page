from manim import *

class DemonVideo(Scene):
    def construct(self):
        # Display the original equation
        equation = MathTex(
            r"\mathbf{x}_{t - \Delta} = \mathbf{x}_t - f_\beta \Delta + g_\beta \mathbf{z} \sqrt{\Delta}"
        )
        self.play(Write(equation))
        self.wait(1)

        # Transform the equation to show the split forms
        split_equations = MathTex(
            r"\mathbf{x}_{t - \Delta}^{(1)} &= \mathbf{x}_t - f_\beta \Delta + g_\beta \mathbf{z}^{(1)} \sqrt{\Delta} \\",
            r"\mathbf{x}_{t - \Delta}^{(2)} &= \mathbf{x}_t - f_\beta \Delta + g_\beta \mathbf{z}^{(2)} \sqrt{\Delta} \\",
            r"\mathbf{x}_{t - \Delta}^{(3)} &= \mathbf{x}_t - f_\beta \Delta + g_\beta \mathbf{z}^{(3)} \sqrt{\Delta} \\",
            r"\vdots \\",
            r"\mathbf{x}_{t - \Delta}^{(K)} &= \mathbf{x}_t - f_\beta \Delta + g_\beta \mathbf{z}^{(K)} \sqrt{\Delta}"
        ).scale(0.9)


        # Animate the transformation
        
        self.play(Transform(equation, split_equations))
        self.wait(2)
        self.play(FadeOut(equation))

#  manim -pqh video.py DemonVideo