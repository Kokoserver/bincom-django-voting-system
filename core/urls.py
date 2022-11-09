from django.urls import path
from . import views

urlpatterns = [
    path("", view=views.index, name="home"),
    path("result/<int:pul_id>", view=views.polling_result, name="polling_result"),
    path("polling_unit/<int:lga_id>", view=views.total_result, name="polling_score"),
    path("addVote/", view=views.addVote, name="addVote"),
]
