from PIL import ImageDraw, Image, ImageChops
import random

def generate_color():
    return list (
        map(lambda x: random.randint(0,255), range(3))
    )

def between_colors(start_color, final_color, factor):
    result = 1 - factor
    return tuple(int(start_color[i] * result + final_color[i] * factor) for i in range(3))

def generate_image(path):

    img_size_px = 128
    padding_px = 16
    img_bg_color = (0, 0, 0)

    start_color, final_color = generate_color(), generate_color()

    image = Image.new("RGB", size=(img_size_px, img_size_px), color=img_bg_color)
    points = list()

    for _ in range(10):
        random_point = (
            random.randint(padding_px, img_size_px - padding_px),
            random.randint(padding_px, img_size_px - padding_px)
        )
        points.append(random_point)

    min_x, max_x = min(p[0] for p in points), max(p[0] for p in points)
    min_y, max_y = max(p[1] for p in points), min(p[1] for p in points)

    delta_x, delta_y = min_x - (img_size_px - max_x), min_y - (img_size_px - max_y)
    for i, point in enumerate(points):
        points[i] = (point[0] - delta_x // 2, point[1] - delta_y // 2)

    thickness = 0
    n_points = len(points) - 1
    
    for i, point in enumerate(points):
        
        cover_image = Image.new("RGB", size=(img_size_px, img_size_px), color=img_bg_color)
        cover_draw  = ImageDraw.Draw(cover_image)

        point1 = point
        point2 = points[0] if i == n_points else points[i+1]

        line_xy = (point1, point2)
        color_factor = i / n_points
        line_color = between_colors(start_color, final_color, color_factor)
        thickness += 1
        cover_draw.line(line_xy, fill=line_color, width=thickness)
        image = ImageChops.add(image, cover_image)

    image.save(path)
    
if __name__ == "__main__":
    generate_image('Image.png')
    