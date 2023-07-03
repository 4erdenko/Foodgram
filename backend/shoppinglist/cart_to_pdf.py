import os
from collections import defaultdict

from django.conf import settings
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO

from shoppinglist.models import ShoppingList


def generate_pdf(user):
    font_path = os.path.join(
        settings.STATIC_ROOT, 'fonts', 'Roboto-Medium.ttf'
    )  # replace with your font file name
    pdfmetrics.registerFont(TTFont('Roboto-Medium', font_path))
    # Словарь для сбора ингредиентов
    ingredients = defaultdict(int)

    # Получаем все списки покупок пользователя
    shopping_lists = ShoppingList.objects.filter(user=user)

    for shopping_list in shopping_lists:
        # Итерируемся по каждому ингредиенту в рецепте,
        # с текущим списком покупок
        for ingredient in shopping_list.recipe.recipeingredient_set.all():
            # Используем defaultdict для автоматического создания
            # нулевого значения, если ключ не существует
            ingredients[str(ingredient.ingredient)] += ingredient.amount

    # Создаем PDF
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    text = p.beginText(70, 700)
    text.setFont('Roboto-Medium', 24)

    for ingredient, quantity in ingredients.items():
        text.textLine(f'{ingredient} — {quantity}')

    p.drawText(text)
    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer
