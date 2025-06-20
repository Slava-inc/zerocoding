from PIL import Image
import os

def images_to_pdf(image_files, output_pdf):
    # Открываем изображения и преобразуем их в формат PDF
    images = [Image.open(f'homework//{image_file}').convert('RGB') for image_file in image_files]

    # Сохраняем изображения в файл PDF
    if images:
        images[0].save(output_pdf, save_all=True, append_images=images[1:])

# Пример использования
image_files = ['C49_1.png', 'C49_2.png', 'C49_3.png', 'C49_4.png', 'C49_5.png']  # Замените на ваши файлы
output_pdf = 'C49.pdf'

images_to_pdf(image_files, output_pdf)