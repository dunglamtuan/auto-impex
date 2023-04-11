from flask import Flask
from flask import Response
import requests
import re, json

app = Flask(__name__)


def getTechnickeUdajeFromRpzv(vin:str, ecv:str):

    file_data = f"""
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/" xmlns:wcf="http://schemas.datacontract.org/2004/07/WcfServiceRPZV" xmlns:dat="http://schemas.datacontract.org/2004/07/DataClass.AppCode">
   <soapenv:Header/>
   <soapenv:Body>
      <tem:GetTechnickeUdajeVozidloPar>
         <!--Optional:-->
         <tem:req>
            <!--Optional:-->
            <wcf:Kontrola>
               <!--Optional:-->
               <dat:DatumOdcitania>2023-01-03T00:00:00</dat:DatumOdcitania>
           
               <!--Optional:-->
               <dat:MileAge>15235</dat:MileAge>
       
               <!--Optional:-->
               <dat:SposobOdcitania>1</dat:SposobOdcitania>
               <!--Optional:-->
               <dat:UnitType>1</dat:UnitType>
               <!--Optional:-->
               <dat:ZivotnaUdalost>DopravnaNehoda</dat:ZivotnaUdalost>
                   <!--Optional:-->
               <dat:ICO>014236546</dat:ICO>
        </wcf:Kontrola>
            <!--Optional:-->
            <wcf:Sender>
               <!--Optional:-->
               <wcf:Name>aaaa</wcf:Name>
               <!--Optional:-->
               <wcf:OrganizacionName>auto-impextest</wcf:OrganizacionName>
               <!--Optional:-->
               <wcf:TypPracoviska>Servis</wcf:TypPracoviska>
            </wcf:Sender>
            <!--Optional:-->
            <wcf:Vozidlo>
              
               <dat:ECV>{ecv}</dat:ECV>
               <dat:VIN>{vin}</dat:VIN>
           
            </wcf:Vozidlo>
            <!--Optional:-->
            <wcf:WsPassword>6dfgeW+a</wcf:WsPassword>
            <!--Optional:-->
            <wcf:WsUser>wsAutoimpex</wcf:WsUser>
         </tem:req>
      </tem:GetTechnickeUdajeVozidloPar>
   </soapenv:Body>
</soapenv:Envelope>
    """

    headers = {"Content-Type": "text/xml;charset=UTF-8", "SOAPAction": "http://tempuri.org/IRPZVStatistic/GetTechnickeUdajeVozidloPar"}
    response = requests.post(data=file_data, url="https://trpzv.iris.sk/WS_ZAPv2/RPZVStatistic.svc",  headers=headers, auth=('wsRPZVuser', 'wsRPZVuser123'))

    return response.text

def rpzvResultToModera(rpzvResult: str):

    return json.dumps({
        "color": re.findall("<Farba>(.*?)</Farba>", rpzvResult)[0],
        "model": re.findall("<Model>(.*?)</Model>", rpzvResult)[0],
        "fuel": re.findall("<Palivo.*>(.*?)</Palivo>", rpzvResult)[0],
        "seats": re.findall("<PocetMiestSedenie>(.*?)</PocetMiestSedenie>", rpzvResult)[0],
        "PrevodovkaPocetStupnov": re.findall("<PrevodovkaPocetStupnov>(.*?)</PrevodovkaPocetStupnov>", rpzvResult)[0],
        "transmissionType": re.findall("<Prevodovka.*>(.*?)</Prevodovka>", rpzvResult)[0],
        "maxPowerKw": re.findall("<VykonMotora.*>(.*?)</VykonMotora>", rpzvResult)[0],
        "cylinderCapacityL": re.findall("<ZdvihovyObjem.*>(.*?)</ZdvihovyObjem>", rpzvResult)[0],
        "make": re.findall("<Znacka.*>(.*?)</Znacka>", rpzvResult)[0],
        "vinCode": re.findall("<VIN.*>(.*?)</VIN>", rpzvResult)[0],
        "Karoseria":re.findall("<Karoseria.*>(.*?)</Karoseria>", rpzvResult)[0]
    })


@app.route('/<vin>')
def xml_format(vin:str):
    '''xml_format'''

    if len(vin) == 7:
        rpzv_result = getTechnickeUdajeFromRpzv('', ecv = vin)
    else :
        rpzv_result = getTechnickeUdajeFromRpzv(vin=vin, ecv='')

    return Response(rpzv_result, mimetype='text/xml')

@app.route('/json/<vin>', methods=['POST'])
def json_format(vin:str):
    '''json_format'''

    if len(vin) == 7:
        rpzv_result = getTechnickeUdajeFromRpzv('', ecv=vin)
    else :
        rpzv_result = getTechnickeUdajeFromRpzv(vin=vin, ecv='')

    return Response(rpzvResultToModera(rpzv_result), mimetype='application/json')

if __name__ == '__main__':
    app.run()
