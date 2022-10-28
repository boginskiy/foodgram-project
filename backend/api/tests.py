# from django.test import TestCase

# Create your tests here.


# для админки
# вербосе наме = ""
# вербосе наме плюрал = ""

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