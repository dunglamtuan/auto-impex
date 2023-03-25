from flask import Flask
from flask import Response
import requests

app = Flask(__name__)


def getTechnickeUdajeFromRpzv(vin:str):

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
                 <dat:SposobOdcitania>1</dat:SposobOdcitania>
                
               <!--Optional:-->
               <dat:UnitType>1</dat:UnitType>
               <!--Optional:-->
               <wcf:MileAge>110829</wcf:MileAge>
               <dat:ZivotnaUdalost>DopravnaNehoda</dat:ZivotnaUdalost>
               <!--Optional:-->
                <dat:ICO>0012345678</dat:ICO>
               </wcf:Kontrola>
            <!--Optional:-->
            <wcf:Sender>
               <!--Optional:-->
               <wcf:Name>test</wcf:Name>
               <!--Optional:-->
               <wcf:OrganizacionName>auto-impextest</wcf:OrganizacionName>
               <!--Optional:-->
               <wcf:TypPracoviska>Poistovna</wcf:TypPracoviska>
            </wcf:Sender>
            <!--Optional:-->
            <wcf:Vozidlo>
               
               <!--Optional:-->
               <dat:VIN>{vin}</dat:VIN>
               <!-- <dat:ECV>BT984EZ</dat:ECV> -->
              
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
    # with open('request.xml', 'rb') as f:
    #   file_data = f.read()

    headers = {"Content-Type": "text/xml;charset=UTF-8", "SOAPAction": "http://tempuri.org/IRPZVStatistic/GetTechnickeUdajeVozidloPar"}
    response = requests.post(data=file_data, url="https://trpzv.iris.sk/WS_ZAPv2/RPZVStatistic.svc",  headers=headers, auth=('wsRPZVuser', 'wsRPZVuser123'))

    #print(type(file_data))
    return response.text


@app.route('/<vin>')
def hello(vin:str):
    return Response(getTechnickeUdajeFromRpzv(vin), mimetype='text/xml')

if __name__ == '__main__':
    app.run()