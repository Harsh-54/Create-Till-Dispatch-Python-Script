import requests
import json
from time import time
from time import sleep
import time
import datetime

def ril_request():
    RIL="http://stgppmpapimum.unicommerce.com/uc/inventory/adjustment/webhook/ril"
    RIL_HEADERS = {
        'Content-Type' : 'application/json',
        'Accept' : 'application/json',
        'ClientId' : 'netmeds',
        'securityKey' : 'test111',
        'merchantID' : 'RIL_NETMEDS'
    }

    FILE="/Users/gyrao/Desktop/RilData/test.txt"


    itr=1
    start=2301
    end=2311
    for i in range(0,1000):
        # startTime = time.time()
        REQUEST='\'{"returnDataCount":10,"returnData":['
        for j in range(start, end):
            REQUEST+='{"itemId":"TestKeshav-'
            REQUEST+=str(i)
            REQUEST+='","fcCode":"RIL_TEST","batchNo":"VEN_BATCH'
            REQUEST+=str(j)
            REQUEST+='","ptr":null,"lastPurchaseCost":90.38333,"averageCost":95.38333,"expiryDate":"2023-07-30","stockQty":8,"mrp":100,"lastUpdated":"2022-10-22T01:10:14.000","lastUpdatedIS":"2022-10-22T01:10:18.100","lastPurchaseDate":"2021-05-17T10:27:28.954","barCode":"76800003035","deleted":false}'
            if j < end-1:
                REQUEST+=','
        REQUEST+=']}\' \n'
        f = open(FILE,"a")
        f.write(REQUEST)
        
        
        itr+=1
        start=end
        end+=10



# exit()

def sale_order_request():
    GET_TOKEN="http://stguat.unicommerce.info/oauth/token?grant_type=password&client_id=uniware-internal-client&username=karun@unicommerce.com&password=uniware"
    CREATE_SALE_ORDER_URL="http://stguat.unicommerce.info/services/rest/v1/oms/saleOrder/create"
    ALLOCATE_INVENTORY_URL="http://stguat.unicommerce.info/data/oms/saleorder/allocate/inventory"
    CREATE_INVOICE_URL="http://stguat.unicommerce.info/services/rest/v1/oms/shippingPackage/createInvoice"
    CREATE_SHIPPING_URL="http://stguat.unicommerce.info/services/rest/v1/oms/shippingPackage/allocateShippingProvider"
    FORCE_DISPATCH="http://stguat.unicommerce.info/services/rest/v1/saleOrderItem/dispatch"
    # MARK_DELIVERED="http://stguat.unicommerce.info/services/rest/v1/saleOrderItem/markDelivered"


    # Get Token
    token = requests.get(GET_TOKEN)
    token = json.loads(token.content)

    HEADERS = {
        'Content-Type' : 'application/json',
        'Authorization' : 'bearer ' + token['access_token'],
        'facility' : '05'
    }


    CREATE_SO=""
    for i in range(1,10001):
        CREATE_SO='{"saleOrder":{"code":"Test-XX-YY-' 
        CREATE_SO+=str(i)
        CREATE_SO+='","channel":"CUSTOM","cashOnDelivery":true,"addresses":[{"id":"19","name":"ABC","addressLine1":"ABC","addressLine2":"XYZ","city":"Delhi","state":"DL","country":"India","pincode":"110020","phone":"9999999999"}],"billingAddress":{"referenceId":"19"},"shippingAddress":{"referenceId":"19"},"saleOrderItems":['

        ITEM=''
        for j in range(1,2):
            ITEM+='{"itemSku":"0211","channelProductId":"0211","channelSaleOrderItemCode":"0211","shippingMethodCode":"STD","code":"0211-' 
            ITEM+=str(j)
            ITEM+='","totalPrice":"100","sellingPrice":"95","facilityCode":"05"}'
            if j<1:
                ITEM+=','
        
        CREATE_SO+=ITEM
        CREATE_SO+=']}}'
        saleOrder = requests.post(CREATE_SALE_ORDER_URL,headers=HEADERS,data=CREATE_SO)
        saleOrder = json.loads(saleOrder.content)
        saleOrderCode=saleOrder['saleOrderDetailDTO']['code']

        ALLO_INV='{"saleOrderCode":"'
        ALLO_INV+=str(saleOrderCode)
        ALLO_INV+='"}'
        allocateInventory = requests.post(ALLOCATE_INVENTORY_URL,headers=HEADERS,data=ALLO_INV)
        allocateInventory = json.loads(allocateInventory.content)
        sleep(1)
        print(allocateInventory)
        shippingPackageCode=allocateInventory['shippingPackageCodes'][0]
        

        INVOICE='{"shippingPackageCode":"'
        INVOICE+=str(shippingPackageCode)
        INVOICE+='","userId":72}'
        invoiceResponse = requests.post(CREATE_INVOICE_URL,headers=HEADERS,data=INVOICE)
        invoiceResponse = json.loads(invoiceResponse.content)

        obj = time.gmtime(0)
        epoch = time.asctime(obj)
        trackingNumber = int(time.time()*1000)
        SHIPPING='{"shippingPackageCode":"'
        SHIPPING+=str(shippingPackageCode)
        SHIPPING+='","shippingProviderCode":"STATUS_TEST","trackingNumber":"'
        SHIPPING+=str(trackingNumber)
        SHIPPING+='"}'
        shippingResponse = requests.post(CREATE_SHIPPING_URL,headers=HEADERS,data=SHIPPING)
        shippingResponse = json.loads(shippingResponse.content)

        DISPATCH='{"shippingPackageCode:"'
        DISPATCH+=str(shippingPackageCode)
        DISPATCH+='","userId":72}'

        ITEMS=''
        for j in range(1,2):
            ITEMS+='"0211-' 
            ITEMS+=str(j)
            ITEMS+='"'
            if j<1:
                ITEMS+=','

        DISPATCH='{"saleOrderCode":"'
        DISPATCH+=str(saleOrderCode)
        DISPATCH+='","saleOrderItemCodes":['
        DISPATCH+=ITEMS
        DISPATCH+=']}'
        dispatchResponse = requests.post(FORCE_DISPATCH,headers=HEADERS,data=DISPATCH)
        print(saleOrderCode)
        # DELIVER='{"saleOrderCode":"'
        # DELIVER+=str(saleOrderCode)
        # DELIVER+='","saleOrderItemCodes":['
        # DELIVER+=ITEMS
        # DELIVER+=']}'
        # requests.post(MARK_DELIVERED,headers=HEADERS,data=DELIVER)
    sleep(1)

sale_order_request()