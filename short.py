from manim import *
import os
import json

# Load data from 'data.json'
with open('data.json', 'r') as f:
    data = json.load(f)

# data['data'] = data['data'][:4]

class ShortVideo(Scene):
    def construct(self):
        # === Title ===
        title = Text("Aligning Diffusion Model by Your Hand", font_size=36)
        title.to_edge(UP)

        # === Reference Image (Left Top) ===
        vertical_image_path = os.path.join('selected_images', 'ref.jpg')
        vertical_image = ImageMobject(vertical_image_path).scale(0.25)
        placeholder_text = Text("Reference", font_size=18).next_to(vertical_image, UP)
        vertical_image_with_label = Group(vertical_image, placeholder_text)
        vertical_image_with_label.to_corner(UL)

        # === Initial Image (Left Bottom) ===
        initial_image_path = os.path.join('selected_images', 'pfode.png')  # Replace with your initial image path
        initial_image = ImageMobject(initial_image_path).scale(0.25)
        initial_image_label = Paragraph(
            "PF-ODE",
            "(0.5414 DINOv2 similarity)", 
            font_size=18,
            alignment='center').next_to(initial_image, UP)
        initial_image_with_label = Group(initial_image, initial_image_label)
        initial_image_with_label.next_to(vertical_image_with_label, DOWN, buff=0.1, aligned_edge=ORIGIN)

        # === Group Left Images ===
        left_images = Group(vertical_image_with_label, initial_image_with_label)

        # === Image Grid Parameters ===
        grid_rows = 4
        grid_cols = 4
        image_size = 8
        spacing = 0.1
        # === Position Content Below Title ===
        left_images.next_to(title, DOWN, buff=0.5, aligned_edge=LEFT)

        # === Loop Through Rounds (Optional) ===
        for idx, round_data in enumerate(data['data']):
            # Create a grid of images for this round
            images = Group()
            for img_path, choice in zip(round_data['images'], round_data['choices']):
                # Create the image
                img = ImageMobject(img_path)
                img.height = image_size / 5
                # Create a surrounding rectangle if the image is selected
                if choice == 1:
                    highlight_rect = Rectangle(
                        width=img.width + 0.05,
                        height=img.height + 0.05,
                        stroke_color=RED,
                        stroke_width=3
                    ).move_to(img)
                    # Group the image and the rectangle
                    img_group = Group(img, highlight_rect)
                else:
                    img_group = img
                images.add(img_group)
            # Arrange images in a grid
            images.arrange_in_grid(rows=grid_rows, cols=grid_cols, buff=spacing)
            images.scale(0.8)
            images.next_to(title, DOWN, buff=0.5, aligned_edge=RIGHT)

            # Animate image grid changes
            if idx == 0:
                self.play(
                    FadeIn(title),
                    FadeIn(left_images),
                    FadeIn(images),
                    run_time=0.5
                )
            elif idx < 5:
                self.play(
                    FadeOut(previous_images), FadeIn(images),
                    run_time=0.5
                )
            else:
                self.play(
                    FadeOut(previous_images), FadeIn(images),
                    run_time=0.25
                )
            previous_images = images
            self.wait(1 if idx == 0 else 0.5 if idx < 5 else 0.25)
    
        final_image_path = os.path.join('selected_images', 'demon.png')  # Replace with your initial image path
        final_image = ImageMobject(final_image_path).scale(0.7)
        final_image_label = Paragraph(
            "Demon",
            "(0.8549 DINOv2 similarity)", 
            font_size=18, 
            alignment='center').next_to(final_image, UP)
        final_image_with_label = Group(final_image, final_image_label)
        final_image_with_label.next_to(title, DOWN, buff=0.5, aligned_edge=RIGHT)
        self.play(FadeIn(final_image_with_label), FadeOut(previous_images), run_time=0.5)
        self.wait(2.5)  # Wait at the end of the video
# manim -qh short.py ShortVideo