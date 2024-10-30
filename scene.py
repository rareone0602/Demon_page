from manim import *

class DemonVideo(Scene):
    def construct(self):
        # Display the original equation
        equation = MathTex(
            r"\mathbf{x}_{t - \Delta}", r"&= \mathbf{x}_t - f_\beta \Delta + g_\beta \mathbf{z} \sqrt{\Delta}"
        )
        self.play(Write(equation))
        self.wait(1)

        # Transform the equation to show the split forms
        split_equations = MathTex(
            r"\mathbf{x}_{t - \Delta}^{(1)}", r" &= \mathbf{x}_t - f_\beta \Delta + g_\beta \mathbf{z}^{(1)} \sqrt{\Delta} \\",
            r"\mathbf{x}_{t - \Delta}^{(2)}", r" &= \mathbf{x}_t - f_\beta \Delta + g_\beta \mathbf{z}^{(2)} \sqrt{\Delta} \\",
            r"\mathbf{x}_{t - \Delta}^{(3)}", r" &= \mathbf{x}_t - f_\beta \Delta + g_\beta \mathbf{z}^{(3)} \sqrt{\Delta} \\",
            r"\vdots \\",
            r"\mathbf{x}_{t - \Delta}^{(K)}", r" &= \mathbf{x}_t - f_\beta \Delta + g_\beta \mathbf{z}^{(K)} \sqrt{\Delta}"
        ).scale(0.9)

        # Animate the transformation
        self.play(Transform(equation, split_equations))
        self.wait(2)

        # Fade out split_equations before starting the transformation into arrows_with_labels
        self.play(FadeOut(split_equations))

        # Create arrows with labels
        arrows_with_labels = Group(
            # Row for x_{t - \Delta}^{1}
            Group(
                MathTex(r"\mathbf{x}_{t - \Delta}^{(1)}"),
                Arrow(LEFT, RIGHT, buff=0.5),
                ImageMobject("assets/SDE_0_1.png").scale(0.1)  # Adjust the scale if needed
            ).arrange(RIGHT, buff=0.5),
            
            # Row for x_{t - \Delta}^{2}
            Group(
                MathTex(r"\mathbf{x}_{t - \Delta}^{(2)}"),
                Arrow(LEFT, RIGHT, buff=0.5),
                ImageMobject("assets/SDE_0_2.png").scale(0.1)
            ).arrange(RIGHT, buff=0.5),

            # Row for x_{t - \Delta}^{3}
            Group(
                MathTex(r"\mathbf{x}_{t - \Delta}^{(3)}"),
                Arrow(LEFT, RIGHT, buff=0.5),
                ImageMobject("assets/SDE_0_3.png").scale(0.1)
            ).arrange(RIGHT, buff=0.5),

            # Dots for intermediate terms
            MathTex(r"\vdots"),

            # Row for x_{t - \Delta}^{K}
            Group(
                MathTex(r"\mathbf{x}_{t - \Delta}^{(K)}"),
                Arrow(LEFT, RIGHT, buff=0.5),
                ImageMobject("assets/SDE_0_K.png").scale(0.1)
            ).arrange(RIGHT, buff=0.5)
        ).arrange(DOWN, buff=0.2).move_to(ORIGIN)

        # Apply TransformFromCopy from split_equations to arrows_with_labels
        self.play(
            TransformFromCopy(split_equations[0], arrows_with_labels[0][0]),  # x_{t - \Delta}^{(1)}
            TransformFromCopy(split_equations[2], arrows_with_labels[1][0]),  # x_{t - \Delta}^{(2)}
            TransformFromCopy(split_equations[4], arrows_with_labels[2][0]),  # x_{t - \Delta}^{(3)}
            TransformFromCopy(split_equations[8], arrows_with_labels[4][0])   # x_{t - \Delta}^{(K)}
        )

        # Adding 'ODE' label over the arrows
        ode_label = Tex(r"ODE").next_to(arrows_with_labels, UP)

        # Display the ODE label
        self.play(Write(ode_label))

        # Optional wait time
        self.wait(2)
