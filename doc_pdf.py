from PIL import Image
import os

def images_to_pdf(image_files, output_pdf):
    # Открываем изображения и преобразуем их в формат PDF
    images = [Image.open(f'homework//{image_file}').convert('RGB') for image_file in image_files]

    # Сохраняем изображения в файл PDF
    if images:
        images[0].save(output_pdf, save_all=True, append_images=images[1:])

# Пример использования
image_files = ['C53_1.png', 'C53_2.png', 'C53_3.png', 'C53_4.png', 'C53_5.png', 'C53_6.png', 'C53_7.png', 'C53_8.png', 'C53_9.png', 'C53_10.png', 'C53_11.png', 'C53_12.png']  # Замените на ваши файлы
output_pdf = 'C53.pdf'

images_to_pdf(image_files, output_pdf)