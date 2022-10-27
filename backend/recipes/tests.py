
#     def update(self, instance, validated_data):
#         """Кастомный метод обновления рецептов."""

#         new_ingred = validated_data.pop('ingredients')
#         current_ingred = instance.ingredients.all()
#         new = len(new_ingred)
#         current = len(current_ingred)
#         n, c = 0, 0

#         while n < new and c < current:

#             if (new_ingred[n]['id'] == current_ingred[c].ingredient.id
#                     and new_ingred[n]['amount'] == current_ingred[c].amount):
#                 n += 1
#                 c += 1
#             else:
#                 instance.ingredients.remove(current_ingred[c].id)

#                 update_rec, status = IngredientRecipe.objects.get_or_create(
#                 ingredient_id=new_ingred[n]['id'], amount=new_ingred[n]['amount'])
#                 instance.ingredients.add(update_rec)

#         while n < new:
#             update_rec, status = IngredientRecipe.objects.get_or_create(
#             ingredient_id=new_ingred[n]['id'], amount=new_ingred[n]['amount'])
#             instance.ingredients.add(update_rec)
#             n += 1

#         while c < current:
#             instance.ingredients.remove(current_ingred[c].id)
#             c += 1