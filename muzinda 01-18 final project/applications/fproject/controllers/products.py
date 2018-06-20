# -*- coding: utf-8 -*-
#This is my app logic->->->@loktioncode 
#this is where you view all products in store
@auth.requires_login()
def view():
    userdict = {}
    users = db(db.auth_user).select()
    for x in users:
        userdict[x.id] = x.first_name + " " + x.last_name
    rows = db(db.products.product_availability=='Available').select(orderby=~db.products.id)
    return locals()

#post products to pizza store
@auth.requires_membership('manager')
def post():
    form = SQLFORM(db.products).process()
    return locals()

##this where i see all products posted by managemnt and update product details #if you did not upload a product yu will see nothing
@auth.requires_membership('manager')
def mypost():
    rows = db(db.products.created_by==session.auth.user.id).select(orderby=db.products.product_availability | ~db.products.id)
    return locals()

#this is where you update posted products #you find the update link in mypost view
@auth.requires_membership('manager')
def update():
    isValid = False
    row = db(db.products.id==request.args(0)).select()
    for x in row:
        if x.created_by==session.auth.user.id:
            isValid =True
    if isValid:
        record = db.products(request.args(0)) or redirect(URL('view'))
        form = SQLFORM(db.products, record)
        if form.process().accepted:
            response.flash = 'Record Updated'
        else:
            response.flash = 'Please Complete the form.'
    return locals()

#add products to cart
@auth.requires_login()
def buy():
    myDict={}
    pizzaRow = db(db.products).select()
    for x in pizzaRow:
        myDict[x.id]= x.product_name
    qty = request.vars.qty
    if qty == None:
        qty = int(1)
    else:
        qty = int(request.vars.qty)
    productId =request.vars.productId
    customer = session.auth.user.id
    db.sale.insert(customer=customer,
                   quantity = qty,
                   productId = productId)
    rows = db(db.sale.customer == session.auth.user.id).select(orderby=~db.sale.id)
    return locals()
#delete products from cart
def delete():
    pizzaRow = db(db.sale.productId==request.args(0)).delete()
    session.flash = 'item has been removed from cart'
    redirect(URL('view'))
    return locals()

#this downloads the product for view
def download():
    return response.download(request, db)

# this sending method ..send order to kitchen as text message 
def send_order():
    return locals() 
#the above code is under construction  
       


