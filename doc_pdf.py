from PIL import Image
import os

def images_to_pdf(image_files, output_pdf):
    # Открываем изображения и преобразуем их в формат PDF
    images = [Image.open(image_file).convert('RGB') for image_file in image_files]

    # Сохраняем изображения в файл PDF
    if images:
        images[0].save(output_pdf, save_all=True, append_images=images[1:])

# Пример использования
image_files = ['C44_0.png', 'C44_1.png', 'C44_2.png', 'C44_3.png', 'C44_4.png', 'C44_5.png', 'C44_6.png', 'C44_7.png']  # Замените на ваши файлы
output_pdf = 'C44.pdf'

images_to_pdf(image_files, output_pdf)