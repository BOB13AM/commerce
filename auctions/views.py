from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import *

def index(request):
    allvalid = listing.objects.filter(closedbid="no").all()
    allclosed = listing.objects.filter(closedbid="yes").all()
    if request.user.is_authenticated:
        #get the user id 
        currentuser= request.user
        current_id = User.objects.get(pk=currentuser.id)

        #gets all the listings for this user
        userlisting = listing.objects.filter(userid=current_id, closedbid="no").all()
        closeduserlisting = listing.objects.filter(userid=current_id, closedbid="yes").all()

        #gets all the user bid if any 
        alluserbids = current_id.userbids.filter(closed="no").all()
        alluserbids_closed = current_id.userbids.filter(closed="yes").all()

        #gets all the user invalid bids if any 
        invalidbids = current_id.invaliduserbids.filter(closed="no").all()
        invalidbids_closed = current_id.invaliduserbids.filter(closed="yes").all()

       

        return render(request, "auctions/index.html", {
            "addmessage": "You dont have any listing yet.",
            "addbidmessage": "You dont have any Bids yet.",
            "addexbidmessage": "You dont have any Expired Bids.",
            #for listing all the user items
            "user_listing": userlisting,
            #for listing all the user closed items
            "closeduser_listing": closeduserlisting,
            #for listing all the bids that made by the user each user is different
            "userbid": alluserbids,
            #for listing all the invalid bids for the user each user is different
            "invalidbid": invalidbids,
            #for listing all the closed items for the user if the user already bid on it
            "closeduserbids": alluserbids_closed,
            #for listing all the closed items for the user if the user bids and the item is invalid for the user 
            "closedinvaliduserbids":invalidbids_closed
        })
    else:
         return render(request, "auctions/index.html", {
            "listingmessage": "Login to see your listing.",
            "bidmessage": "Login to see your Bids",
            "exbidmessage": "Login to see your Expired Bids"
        })


def listingall(request):

    allvalid = listing.objects.filter(closedbid="no").all()
    allclosed = listing.objects.filter(closedbid="yes").all()
    return render(request, "auctions/listingall.html",{
            #for listing all the items available fromall users
            "all_listing": allvalid,
            #for listing all the closed items from all the users (might change later)
            "closed_listing": allclosed
    })
            

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("commerce:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("commerce:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("commerce:index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def delete(request):
    if request.method == "POST":
        id = request.POST.get('deleteid')
        if id:
            d = listing.objects.get(pk=int(id))
            d.delete()
            return HttpResponseRedirect(reverse("commerce:index"))
        else:
             return render(request, "auctions/index.html", {
                "message": "Something went wrong while deleting."
            })
    else:
        all = listing.objects.all()

        return render(request, "auctions/index.html", {
            "all_listing": all
        })


def create(request):
    if request.user.is_authenticated:
        if request.method == "POST":

            title = request.POST.get('title')
            description = request.POST.get('description')
            bid = request.POST.get('bid')
            category = request.POST.get('category')
            img = request.POST.get('image')

            if not title or not bid or not description:
                return render(request, "auctions/create.html", {
                "message": "You should fill up all the required  fields *"
            })
                        
            min_bid = float(bid)

            if not img and not category:
                img = "https://i.ibb.co/crFzJzG/No-image.jpg"
                new = listing(title=title, description=description,  image=img, bid=min_bid, userid=request.user, closedbid="no")
                new.save()
                return HttpResponseRedirect(reverse("commerce:index"))
            elif not img:
                img = "https://i.ibb.co/crFzJzG/No-image.jpg"
                new = listing(title=title, description=description, category=category, image=img, bid=min_bid, userid=request.user, closedbid="no")
                new.save()
                return HttpResponseRedirect(reverse("commerce:index"))
            elif not category :
                new = listing(title=title, description=description, image=img, bid=min_bid, userid=request.user, closedbid="no")
                new.save()
                return HttpResponseRedirect(reverse("commerce:index"))
            else:            
                new = listing(title=title, description=description, category=category, image=img, bid=min_bid, userid=request.user, closedbid="no")
                new.save()
                return HttpResponseRedirect(reverse("commerce:index"))          
        else:
            return render(request, "auctions/create.html")
    else:  
        return render(request, "auctions/login.html", {
            "message": "You should login first, to be able to add a listing."
        })

def listingpage(request, page_id):
    if request.user.is_authenticated:
     #get the user id 
     currentuser= request.user
     current_id = User.objects.get(pk=currentuser.id)   
     if request.method == "POST":
        listingid = int(page_id)
        item = listing.objects.get(pk=listingid)
        #gets all the comments of the items
        allcomments = comments.objects.all()
        #get the reply from commentreply table
        allreply=commentreply.objects.all()  

        return render(request, "auctions/listingpage.html", {
            #for comments of all items
            "all_comments": allcomments,
            "current_user": currentuser,
            "pageitem":item,
            "reply": allreply
        })

     else:
        listingid = int(page_id)
        item = listing.objects.get(pk=listingid)
        #gets all the comments of the items
        allcomments = comments.objects.all()
        #get the reply from commentreply table
        allreply=commentreply.objects.all()
        return render(request, "auctions/listingpage.html", {
             #for comments of all items
            "all_comments": allcomments,
            "current_user": currentuser,
            "pageitem":item,
            "reply": allreply   
        })
    else:
        return render(request, "auctions/login.html", {
            "message": "You should login first, to be able to Explore Listings."
        })

def wish(request):
    if request.user.is_authenticated:
        userid = User.objects.get(pk=request.user.id)
        if request.method == "POST":
            itemid = request.POST.get('wishid')
            deleteid = request.POST.get('deletewishid')
            if itemid:
                wishitem = listing.objects.get(pk=int(itemid))
                wishitem.wishlist.add(userid)
                allwishitems = userid.wishlistings.all()
                return HttpResponseRedirect(reverse("commerce:wish"))
                
            elif deleteid:
                wishitem = listing.objects.get(pk=int(deleteid))
                wishitem.wishlist.remove(userid)
                allwishitems = userid.wishlistings.all()
                return HttpResponseRedirect(reverse("commerce:wish")) 

        else:
            allwishitems = userid.wishlistings.filter(closedbid="no").all()
            allwishitems_closed = userid.wishlistings.filter(closedbid="yes").all()
            return render(request, "auctions/wish.html",{
                "allitems":allwishitems,
                "closedwish": allwishitems_closed
            })
        
    else:
        return render(request, "auctions/login.html", {
            "message": "You should login first, to be able to check your wishlist."
        })                  

def bidfunc(request):
    if request.user.is_authenticated:
        userid = User.objects.get(pk=request.user.id)
        if request.method == "POST":
            itemid = request.POST.get('bidid')
            bidamount = request.POST.get('bid')
            deleteid = request.POST.get('deleteid')
                       
            #delete user bid
            if deleteid and itemid:
                #delete the current bid from the table 
                item = listing.objects.get(pk=int(itemid))     
                item.currentbid = None
                item.save()

                #get the item by id and delete it
                intdeleteid = int(deleteid)
                deleteitem = bids.objects.get(pk=intdeleteid)
                deleteitem.delete()

                #return to the index function
                return HttpResponseRedirect(reverse("commerce:index")) 


            # if check for validity
            if not itemid or not bidamount:
                all = listing.objects.all()    
                return render(request, "auctions/listingall.html", {
                    "message": "Missing Bid or Item!",
                    "all_listing":all
                })        

            #bid amount from user convert it to int
            floatbid = float(bidamount)
            #item id from user convert it to int
            intid = int(itemid)

            #get the item from listing table    
            item = listing.objects.get(pk=intid)
            #get the price of the item and convert it to int
            itemprice = float(item.bid)
           
            if bids.objects.filter(itembid=item):
                #get the current bid of the item if any 
                biditem = bids.objects.get(itembid=item)
                currentbid = float(biditem.biding)
                if floatbid > currentbid:

                    #saving the invalid old bid in invalidbid table   
                    user_biditem = biditem.userbid
                    item_biditem = biditem.itembid
                    bid_biditem = biditem.biding
                    oldbid = invalidbid(invalid_userbid=user_biditem, invalid_itembid=item_biditem, invalid_biding=bid_biditem, closed="no")
                    oldbid.save()

                    #deleting the old bid 
                    biditem.delete()

                    #inserting the new bid in the bids table
                    newbid = bids(userbid=request.user, itembid=item, biding=floatbid, closed = "no")
                    newbid.save()

                    #get the current bid of the item if any 
                    biditem = bids.objects.get(itembid=item)
                    newcurrentbid = biditem.biding

                    #add the new current bid to listing 
                    item.currentbid = None
                    item.currentbid = newcurrentbid
                    item.save()

                    #add the new current winning user
                    item.winninguser = None
                    #add the new current winner
                    item.winninguser = userid
                    item.save()
                    
                    #return to the listingall function
                    return HttpResponseRedirect(reverse("commerce:index")) 
                else:
                    allvalid = listing.objects.filter(closedbid="no").all()
                    allclosed = listing.objects.filter(closedbid="yes").all()
                    return render(request, "auctions/listingall.html",{
                            "message":"Your bid is less than or equal to the current bid",
                            #for listing all the items available fromall users
                            "all_listing": allvalid,
                            #for listing all the closed items from all the users (might change later)
                            "closed_listing": allclosed
                    })        
            elif itemprice:
                if floatbid > itemprice:
                    #inserting the new bid in the new table 
                    add = bids(userbid=request.user, itembid=item, biding = floatbid, closed="no")
                    add.save()

                    #add the new current bid
                    item.currentbid = floatbid
                    item.save()

                    #add the new current winner
                    item.winninguser = userid
                    item.save()

                    #return to the listingall function
                    return HttpResponseRedirect(reverse("commerce:index")) 
                    
                else:
                    allvalid = listing.objects.filter(closedbid="no").all()
                    allclosed = listing.objects.filter(closedbid="yes").all()
                    return render(request, "auctions/listingall.html",{
                            "message":"Your bid is less than or equal to the item price",
                            #for listing all the items available fromall users
                            "all_listing": allvalid,
                            #for listing all the closed items from all the users (might change later)
                            "closed_listing": allclosed
                    })  
            else:
                return render(request, "auctions/listingall.html", {
                            "message":"something went wrong" 
                        })

        else:
            #return to the listingall function
            return HttpResponseRedirect(reverse("commerce:index"))  
    else:    
        return render(request, "auctions/login.html", {
            "message": "You should login first, to be able to place a bid."
        })



@login_required
def invalidbidfunc(request):
    if request.method == "POST":
        deleteid = request.POST.get('deleteid')

        if deleteid:
            #get the expired item and delete it
            expireditem = invalidbid.objects.get(pk=int(deleteid))
            expireditem.delete()
            #return to the index function
            return HttpResponseRedirect(reverse("commerce:index"))
    else:
        #return to the index function
        return HttpResponseRedirect(reverse("commerce:index"))    



def closedbids(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            closeid = request.POST.get('closeid')
            if closeid:
                #close the item in listing table
                intcloseid = int(closeid)
                item = listing.objects.get(pk=intcloseid)
                item.closedbid = "yes"
                item.save()

                #close the item in bids table
                if bids.objects.filter(itembid=item):
                    #get the item from listing and then filter it in bids to change the closed field from no to yes
                    item = listing.objects.get(pk=intcloseid)
                    biditem = bids.objects.get(itembid=item)
                    biditem.closed = None
                    biditem.closed = "yes"
                    biditem.save()
                
                if invalidbid.objects.filter(invalid_itembid=item):
                    #get the item from listing and then filter it in invalidbids to change the closed field from no to yes
                    item = listing.objects.get(pk=intcloseid)
                    invalidbiditem = invalidbid.objects.get(invalid_itembid=item)
                    invalidbiditem.closed=None
                    invalidbiditem.closed="yes"
                    invalidbiditem.save()

                if not invalidbid.objects.filter(invalid_itembid=item) and not bids.objects.filter(itembid=item):
                    item.currentbid = 0
                    item.save()      

                #return to the index function
                return HttpResponseRedirect(reverse("commerce:index"))
            else:
                #return to the index function
                return HttpResponseRedirect(reverse("commerce:index"))     


    else:
        allclosed = listing.objects.filter(closedbid="yes").all()
        return render(request, "auctions/closedbids.html", {
            "closedmessage": "No Closed Bids.",
            "all_listing":allclosed
        }) 


def commentsfunc(request):
    if request.user.is_authenticated:
        userid = User.objects.get(pk=request.user.id)
        if request.method == "POST":
            itemid = request.POST.get('id')
            user_comment = request.POST.get('comment')
            deleteid = request.POST.get('deleteid')

            if deleteid and itemid:
                intitemid = int(itemid)
                intdeleteid = int(deleteid)
                d = comments.objects.get(pk=intdeleteid)
                d.delete()
                #return to the index function
                return HttpResponseRedirect(reverse(("commerce:listingpage"), args=(intitemid,)))
               
            if user_comment and itemid:
                intitemid = int(itemid)
                item = listing.objects.get(pk=intitemid)
                add = comments(usercomment=userid, itemcomment=item, comment=user_comment)
                add.save()
                #return to the listingpage function
                return HttpResponseRedirect(reverse(("commerce:listingpage"), args=(intitemid,)))
            else:        
                #return to the index function
                return HttpResponseRedirect(reverse("commerce:index"))
        
        else:        
            #return to the index function
            return HttpResponseRedirect(reverse("commerce:listingall"))
    
    
    else:
         return render(request, "auctions/login.html", {
            "message": "You should login first, to be able to Comment.",
        })        


def reply(request):
    if request.user.is_authenticated:
        userid = User.objects.get(pk=request.user.id)
        if request.method == "POST":
            maincommentid = request.POST.get("commentid")
            replycomment = request.POST.get("reply")
            newreply = request.POST.get("newreply")
            olduser = request.POST.get("olduser")
            oldreply = request.POST.get("oldreply")
            pageid=request.POST.get("pageid")
            intpageid=int(pageid)
            if maincommentid and replycomment and not olduser and not oldreply:
                main_comment = comments.objects.get(pk=int(maincommentid))
                add = commentreply(replying_user_main=userid, maincomment=main_comment, reply=replycomment)
                add.save()
            elif maincommentid and newreply and olduser and oldreply:
                main_comment = comments.objects.get(pk=int(maincommentid))
                old_user = User.objects.get(username=olduser)
                add = commentreply(replying_user_main=userid, maincomment=main_comment, reply=newreply, old_replying_user=old_user, old_reply=oldreply)
                add.save()

            return HttpResponseRedirect(reverse(("commerce:listingpage"), args=(intpageid,)))
        else:
            return HttpResponseRedirect(reverse("commerce:index"))    
    else:
         return render(request, "auctions/login.html", {
            "message": "You should login first, to be able to Reply.",
        })


def category(request, category_name):
    fetchcategory = listing.objects.filter(category=category_name, closedbid="no").all()
    name = category_name
    return render(request, "auctions/category.html", {
           "all_listing":fetchcategory,
           "name":name
        }) 

