
# -----------------------------------------------------
#         new_ingr = validated_data.pop('ingredients')
#         curr_ingr = instance.ingredients.all()

# # new_ingred
# # [OrderedDict([('id', 1), ('amount', 77.0)]), OrderedDict([('id', 100), ('amount', 78.0)])]
# # [{'id': 12, 'amount': 77.0}, {'id': 13, 'amount': 78.0}]
#         count_new_ingr= len(new_ingr)
#         count_curr_ingr = len(curr_ingr)
#         i, k = 0, 0

#         while i < count_new_ingr and k < count_curr_ingr:

#             if (new_ingr[i]['id'] == curr_ingr[k].id and
#                     new_ingr[i]['amount'] == curr_ingr[k].amount):
#                 i += 1
#                 k += 1
#             else:
#                 instance.ingredients.remove(curr_ingr[k].id)
#                 k += 1

#         while k < count_curr_ingr:
#             instance.ingredients.remove(curr_ingr[k].id)

#         while i < count_new_ingr:
#             update_rec, status = IngredientRecipe.objects.get_or_create(
#             ingredient_id=new_ingr[i]['id'], amount=new_ingr[i]['amount'])
#             instance.ingredients.add(update_rec)

# --------------------------------------------------
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
# ----------------------------
 # Димон делал
#  if new_ingred:

#             # clean recipes ing
#             for obj in current_ingred:
#                 obj.recipe_set.remove(instance)

#             for new_ing in new_ingred:
#                 update_rec, status = IngredientRecipe.objects.get_or_create(
#                 ingredient_id=new_ing['id'], amount=new_ing['amount'])
#                 instance.ingredients.add(update_rec)
#         else:
#             for cur_ing in current_ingred:
#                 instance.ingredients.add(cur_ing)
# ----------------------------

# Create your tests here.


# для админки
# вербосе наме = ""
# вербосе наме плюрал = ""


