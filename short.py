from manim import *
import os

class ShortVideo(Scene):
    def construct(self):
        # === Title ===
        title = Text("Aligning Diffusion Model by Manual Selection", font_size=36)
        title.to_edge(UP)

        # === Vertical Image ===
        vertical_image_path = os.path.join('selected_images', 'ref.jpg')
        vertical_image = ImageMobject(vertical_image_path).scale(0.5)
        placeholder_text = Text("Reference", font_size=24).next_to(vertical_image, DOWN)
        vertical_image.add(placeholder_text)
 
        # === Double Directional Arrow with Label ===
        arrow_length = 2
        arrow = DoubleArrow(start=LEFT * arrow_length / 2, end=RIGHT * arrow_length / 2, buff=0)
        arrow.set_color(YELLOW)

        # Label above the arrow
        arrow_label = Text("DINOv2 similarity", font_size=18)
        arrow_label.next_to(arrow, UP)

        # Group arrow and label using Group for better performance
        arrow_group = VGroup(arrow, arrow_label)

        # === Image Grid Parameters ===
        images_dir = "./selected_images"  # Ensure this directory exists and contains images
        grid_rows = 4  # Reduced from 16 for better performance
        grid_cols = 4  # Reduced from 16 for better performance
        image_size = 0.2  # Adjusted for smaller grid
        spacing = 0.05

        # Load images
        image_files = []
        if os.path.exists(images_dir):
            # Sorted for consistent ordering
            for file in sorted(os.listdir(images_dir)):
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                    image_files.append(os.path.join(images_dir, file))
        else:
            image_files = []

        # Limit to grid size
        max_images = grid_rows * grid_cols
        image_files = image_files[:max_images]

        # Create grid of images
        images = Group()
        for idx, img_path in enumerate(image_files):
            try:
                img = ImageMobject(img_path).scale(image_size)
            except Exception:
                # Handle corrupted images or unsupported formats
                img = Square(side_length=image_size).set_color(GREY)
                error_text = Text("Err", font_size=6)
                img.add(error_text)
            
            # Highlight selected images (e.g., every 10th)
            if idx % 2 == 0:
                img.set_stroke(RED)
            
            images.add(img)

        # Fill remaining grid with placeholders if necessary
        total_images = grid_rows * grid_cols
        for _ in range(len(images), total_images):
            placeholder = Square(side_length=image_size).set_color(GREY)
            empty_text = Text("Empty", font_size=6)
            placeholder.add(empty_text)
            images.add(placeholder)

        # Arrange images in grid
        images.arrange_in_grid(rows=grid_rows, cols=grid_cols, buff=spacing)

        # === Arrange Horizontal Layout ===
        horizontal_group = Group(
            vertical_image,
            arrow_group,
            images
        ).arrange(RIGHT, buff=0.5)

        # Position below the title
        horizontal_group.next_to(title, DOWN, buff=1)

        # === Add Elements to Scene with Animations ===
        self.play(FadeIn(title), FadeIn(vertical_image), FadeIn(arrow_group), FadeIn(images))
        self.wait(2)

# manim -pql short.py ShortVideo