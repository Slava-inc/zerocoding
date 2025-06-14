from PIL import Image
import os

def images_to_pdf(image_files, output_pdf):
    # Открываем изображения и преобразуем их в формат PDF
    images = [Image.open(f'homework//{image_file}').convert('RGB') for image_file in image_files]

    # Сохраняем изображения в файл PDF
    if images:
        images[0].save(output_pdf, save_all=True, append_images=images[1:])

# Пример использования
image_files = ['C46_1.png', 'C46_2.png', 'C46_3.png', 'C46_4.png', 'C46_5.png', 'C46_6.png', 'C46_7.png']  # Замените на ваши файлы
output_pdf = 'C46.pdf'

images_to_pdf(image_files, output_pdf)