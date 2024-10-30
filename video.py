from manim import *

class DemonVideo(Scene):
    def construct(self):
        self.show_original_equation()
        self.transform_to_split_equations()
        self.transition_to_arrows_with_labels()
        self.apply_human_evaluation()
        self.back_to_equation()
        self.final_plug_in()
        # self.next_section()
        self.demonstration_end()
    
    def show_original_equation(self):
        # Display the original equation
        self.current_equation = MathTex(
            r"\mathbf{x}_{t - \Delta}", r"=", r"\mathbf{x}_t -", r"f_\beta \Delta", r"+", r"g_\beta \mathbf{z} \sqrt{\Delta}"
        )
        
        # Title "Diffusion Model" above the equation
        title = Tex("A Diffusion Model SDE Step").next_to(self.current_equation, UP)

        # Underbrace for "Drift" and "Diffusion" parts
        drift_underbrace = Brace(self.current_equation[3], color=BLUE)
        drift_label = MathTex(r"\text{Drift}").next_to(drift_underbrace, DOWN)
        
        diffusion_underbrace = Brace(self.current_equation[5], color=GREEN)
        diffusion_label = MathTex(r"\text{Diffusion}").next_to(diffusion_underbrace, DOWN)

        # Display the title, equation, and underbraces with labels
        self.play(Write(title), Write(self.current_equation))
        self.play(Write(drift_underbrace), Write(drift_label))
        self.play(Write(diffusion_underbrace), Write(diffusion_label))
        self.wait(1)
        self.play(FadeOut(title), FadeOut(drift_underbrace), FadeOut(drift_label), FadeOut(diffusion_underbrace), FadeOut(diffusion_label))

    def transform_to_split_equations(self):
        self.split_equations = MathTex(
            r"\mathbf{x}_{t - \Delta}^{(1)}", r"&=", r"\mathbf{x}_t - f_\beta \Delta + g_\beta", r"\mathbf{z}^{(1)}", r"\sqrt{\Delta} \\",
            r"\mathbf{x}_{t - \Delta}^{(2)}", r"&=", r"\mathbf{x}_t - f_\beta \Delta + g_\beta", r"\mathbf{z}^{(2)}", r"\sqrt{\Delta} \\",
            r"\mathbf{x}_{t - \Delta}^{(3)}", r"&=", r"\mathbf{x}_t - f_\beta \Delta + g_\beta", r"\mathbf{z}^{(3)}", r"\sqrt{\Delta} \\",
            r"\vdots \\",
            r"\mathbf{x}_{t - \Delta}^{(K)}", r"&=", r"\mathbf{x}_t - f_\beta \Delta + g_\beta", r"\mathbf{z}^{(K)}", r"\sqrt{\Delta}"
        )

        title = Tex("i.i.d. Sampling").next_to(self.split_equations, UP)

        # Animate the transformation from the original equation to the split equations
        self.play(FadeIn(title))
        self.play(ReplacementTransform(self.current_equation, self.split_equations))

        # Highlight the z terms in each equation

        self.z_terms = [self.split_equations[3], self.split_equations[8], self.split_equations[13], self.split_equations[19]]
        self.x_terms_eq = [self.split_equations[0], self.split_equations[5], self.split_equations[10], self.split_equations[16]]

        self.play(*[Indicate(z_term) for z_term in self.z_terms])
        self.wait(1)
        self.play(FadeOut(title))

    def transition_to_arrows_with_labels(self):
        # Create arrows and labels for each split equation
        self.arrows_with_labels = []

        # Process equations for i = 1 to 3
        for i in range(1, 4):
            image_path = f"assets/SDE_0_{i}.png"
            evaluation = "-1" if i % 2 == 1 else "+1"
            evaluation_color = BLUE if evaluation == "-1" else RED

            # Create components
            x_term = self.x_terms_eq[i - 1].copy()  # \mathbf{x}_{t - \Delta}^{(i)}
            arrow = Arrow(LEFT, RIGHT, buff=0.2)
            r_label = MathTex(r"r(")
            image = ImageMobject(image_path).scale(0.1)
            closing_parenthesis = MathTex(r") =")
            evaluation_label = MathTex(evaluation).set_color(evaluation_color)

            # Group components
            group = Group(
                x_term, arrow, r_label, image, closing_parenthesis, evaluation_label
            ).arrange(RIGHT, buff=0.5)

            self.arrows_with_labels.append(group)

        # Add the ellipsis
        dots = MathTex(r"\vdots")
        self.arrows_with_labels.append(dots)

        # Process the equation for i = K
        equation_K = self.split_equations[-1]  # Last equation
        image_path_K = "assets/SDE_0_K.png"
        evaluation_K = "+1"
        evaluation_color_K = RED

        x_term_K = self.x_terms_eq[3].copy()  # \mathbf{x}_{t - \Delta}^{(K)}
        arrow_K = Arrow(LEFT, RIGHT, buff=0.2)
        r_label_K = MathTex(r"r(")
        image_K = ImageMobject(image_path_K).scale(0.1)
        closing_parenthesis_K = MathTex(r") =")
        evaluation_label_K = MathTex(evaluation_K).set_color(evaluation_color_K)

        group_K = Group(
            x_term_K, arrow_K, r_label_K, image_K, closing_parenthesis_K, evaluation_label_K
        ).arrange(RIGHT, buff=0.5)

        self.arrows_with_labels.append(group_K)

        # Arrange all groups vertically
        self.arrows_with_labels_group = Group(*self.arrows_with_labels).arrange(DOWN, buff=0.5)

        # Animate the transition from split equations to arrows with labels
        transforms = []
        for i, group in enumerate(self.arrows_with_labels):
            if isinstance(group, Group):
                j = i if i < 3 else 3
                transforms.append(TransformFromCopy(self.x_terms_eq[j], group[0]))  # x_{t - \Delta}^{(i)}
        
        self.play(FadeOut(self.split_equations), *transforms)

        self.evaluation_labels = [group[5] for group in self.arrows_with_labels if isinstance(group, Group)]

        # Animate arrows, images, and labels
        self.to_plays = []
        for group in self.arrows_with_labels:
            if isinstance(group, Group):
                arrow = group[1]
                ode_text = Tex(r"ODE").next_to(arrow, UP)
                self.play(Write(arrow), Write(ode_text), FadeIn(group[3]))  # group[3] is the image
                self.to_plays.append(FadeOut(ode_text))
            else:
                # Handle the "vdots"
                self.play(Write(group))
        
        self.play(*self.to_plays)

    def apply_human_evaluation(self):
        # Write the r labels and evaluations
        self.to_plays = []
        for group in self.arrows_with_labels:
            if isinstance(group, Group):
                self.to_plays.extend([Write(group[2]), Write(group[4]), Write(group[5])])
        
        self.play(*self.to_plays)
        self.wait(1)

    def back_to_equation(self):
        # x_terms => x_terms_eq
        # evaluation_labels => z_terms
        # color failed to match evaluation_labels
        self.compute_z_star = MathTex(
            r"\mathbf{z}^*", # 0
            r"=", # 1
            r"\frac{1}{\sqrt{K}} \left(", # 2
            r"-1", # 3
            r"\cdot \mathbf{z}^{(1)}", # 4 
            r"+1", # 5 
            r"\cdot \mathbf{z}^{(2)}", # 6
            r"-1", # 7
            r"\cdot \mathbf{z}^{(3)}", # 8
            r"\cdots", # 9
            r"+1", # 10 
            r"\cdot \mathbf{z}^{(K)}", # 11
            r"\right)" # 12
        )
        self.z_terms_in_z_star = [self.compute_z_star[i] for i in [4, 6, 8, 11]]
        self.z_labels_in_z_star = [self.compute_z_star[i] for i in [3, 5, 7, 10]]

        # Set colors for MathTex objects (evaluation labels are not images, so no error will occur here)
        for label_in_z_star, label in zip(self.z_labels_in_z_star, self.evaluation_labels):
            label_in_z_star.set_color(label.get_color())

        self.equation_groups = VGroup(self.split_equations, self.compute_z_star).arrange(DOWN, buff=0.5)
        
        fade_out_transforms = []
        transforms = []
        
        for i, group in enumerate(self.arrows_with_labels):
            if isinstance(group, Group):
                j = i if i < 3 else 3
                transforms.append(ReplacementTransform(group[0], self.x_terms_eq[j])) 
                fade_out_transforms.append(FadeOut(group[1])) # arrow
                fade_out_transforms.append(FadeOut(group[2])) # r_label
                fade_out_transforms.append(FadeOut(group[3])) # image
                fade_out_transforms.append(FadeOut(group[4])) # closing_parenthesis
                transforms.append(ReplacementTransform(self.evaluation_labels[j], self.z_labels_in_z_star[j]))
            else:
                fade_out_transforms.append(FadeOut(group))
                

        # Make sure that you only fade out vectorized objects (not ImageMobjects)
        self.play(*fade_out_transforms, *transforms)

        texts_to_write = VGroup(*[
            text for text in self.equation_groups[0]
            if text not in self.x_terms_eq
        ])
        
        self.play(Write(texts_to_write))

        transforms = []
        for z_1, z_2 in zip(self.z_terms, self.z_terms_in_z_star):
            transforms.append(TransformFromCopy(z_1, z_2))
        self.play(*transforms)

        self.wait(1)
        
        texts_to_write = VGroup(*[
            text for text in self.equation_groups[1]
            if not (text in self.z_terms_in_z_star or text in self.z_labels_in_z_star)
        ])
        self.play(Write(texts_to_write))
        self.play(Indicate(self.compute_z_star[0]))
        self.play(FadeToColor(self.compute_z_star[0], PURPLE))

        self.wait(1)
    
    def final_plug_in(self):
        self.final_equation = MathTex(
            r"\mathbf{x}_{t - \Delta}", r"&=", r"\mathbf{x}_t - f_\beta \Delta + g_\beta",  r"\mathbf{z}^*", r"\sqrt{\Delta}"
        )
        self.final_equation[3].set_color(PURPLE)
        title = Tex("A Diffusion Model ", "Demon", " Step").next_to(self.final_equation, UP)
        title[1].set_color(PURPLE)
        self.play(TransformFromCopy(self.compute_z_star[0], self.final_equation[3]), FadeOut(self.equation_groups))
        self.play(FadeIn(title))
        self.play(Write(VGroup(*[self.final_equation[i] for i in range(len(self.final_equation)) if i != 3])))
        self.wait(1)
        self.play(FadeOut(title), FadeOut(self.final_equation))
    
    def demonstration_end(self):
        
        self.illustration_eq = MathTex(
            r"\mathbf{x}_t", r"\xrightarrow{\mathbf{z}_t}",
            r"\mathbf{x}_{t - \Delta_1}", r"\xrightarrow{\mathbf{z}_{t - \Delta_1}}",
            r"\cdots",
            r"\mathbf{x}_{t - \Delta_T}", r"\xrightarrow{\mathbf{z}_{t - \Delta_T}}",
            r"\mathbf{x}_0 = "
        )

        title = Tex("Sampling Demon").next_to(self.illustration_eq, UP)
        self.illustration_eq[1].set_color(PURPLE)
        self.illustration_eq[3].set_color(PURPLE)
        self.illustration_eq[6].set_color(PURPLE)
        # Group eq and assets/demon.jpg
        self.illustration = Group(self.illustration_eq, ImageMobject("assets/demon.jpg").scale(0.2)).arrange(RIGHT, buff=0.5)
        
        self.play(FadeIn(title))
        self.play(Write(self.illustration_eq[:-1]))
        self.wait(.5)
        self.play(FadeIn(self.illustration_eq[-1]), FadeIn(self.illustration[-1]))
        self.wait(5)

# manim -pql video.py DemonVideo
# Output gif:
# manim -pql video.py DemonVideo -s