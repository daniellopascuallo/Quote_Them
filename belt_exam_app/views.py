from django.shortcuts import render, redirect

from .models import User, Quote

from django.contrib import messages

import bcrypt

def index(request):

    return render(request, "index.html")

# method to validate:
def registration(request):
    print(request.POST)
    errorsObject = User.objects.registrationValidator(request.POST)

    if len(errorsObject) > 0:
        for value in errorsObject.values():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect("/")

    else: # register user
        # encrypt the password and then register user
        password = request.POST["form_password"]
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        
        # register user but with encrypted password, not the one from the form
        newUser = User.objects.create(first_name= request.POST["form_first_name"], last_name= request.POST["form_last_name"], email= request.POST["form_email"], password= pw_hash)
        # keep new user logged in, in session: store newUser.id in request.session with a key value pair (session is a dict). It is only the id not the whole object
        request.session["userLoggedIn"] = newUser.id
        return redirect("/quotes")
##############################################


# method to validate:
def login(request):
    print(request.POST)
    # send request.POST to validator (function call)
    errorsObject = User.objects.loginValidator(request.POST)

    if len(errorsObject) > 0:
        for value in errorsObject.values():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect("/")
    
    else:
        userLogIn = User.objects.filter(email= request.POST["form_email"])
        request.session["userLoggedIn"] = userLogIn[0].id
        return redirect("/quotes")
###################################################


def quotes(request):
    if "userLoggedIn" not in request.session:
        messages.error(request, "Please, log in first")
        return redirect("/")

    context = {
        "userLoggedIn" : User.objects.get(id= request.session["userLoggedIn"]),
        "allQuotes" : Quote.objects.all(),

    }

    return render(request, "quotes.html", context)


# post, method to validate:
def add_quote(request):
    print(request.POST)
    errorsObject = Quote.objects.quoteValidator(request.POST)

    if len(errorsObject) > 0:
        for value in errorsObject.values():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect("/quotes")

    else:
        new_quote= Quote.objects.create(author= request.POST["form_author"], content= request.POST["form_content"], user= User.objects.get(id= request.session["userLoggedIn"]))

        return redirect("/quotes")
#########################################################

def logout(request):
    request.session.clear()
    return redirect("/")


def user_quotes(request, userID):
    
    context = {
        "addedQuotes" : Quote.objects.filter(user= userID),
        "userLoggedIn" : User.objects.get(id= request.session["userLoggedIn"]),
        "userWhoQuoted" : User.objects.get(id= userID)
    }
    return render(request, "user_quotes.html", context)


def like_quote(request, quoteID):
    # get ids of user and quote:
    one_user = User.objects.get(id= request.session["userLoggedIn"])
    one_quote = Quote.objects.get(id= quoteID)
    # many to many join 
    one_quote.likes.add(one_user)
    return redirect("/quotes")


def delete_quote(request, quoteID):
    quote_to_delete = Quote.objects.get(id= quoteID)
    quote_to_delete.delete()
    return redirect("/quotes")


def edit_account(request, userID):
    context = {
        "userInfo" : User.objects.get(id= userID) 
    }
    return render(request, "edit_account.html", context)

# method to validate
def update_account(request, userID):
    print(request.POST)

    errorsObject = User.objects.accountValidator(request.POST)

    if len(errorsObject) > 0:
        for value in errorsObject.values():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect(f"/edit/{userID}")

    else:
        edited_account = User.objects.get(id= userID)
        edited_account.first_name = request.POST["form_first_name"]
        edited_account.last_name = request.POST["form_last_name"]
        edited_account.email = request.POST["form_email"]
        edited_account.save()
        return redirect(f"/edit/{userID}")
###################################
