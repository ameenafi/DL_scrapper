import requests
from lxml import html
import json

url = 'https://parivahan.gov.in/rcdlstatus/?pur_cd=101'

def get_captcha():
    cap=tree.xpath('//img[@id="form_rcdl:j_idt34:j_idt41"]/@src')
    captcha='https://www.parivahan.gov.in'+cap[0]
    r=requests.get(captcha)
    open('Captcha.jpg', 'wb').write(r.content)
    captcha_code=input('enter the Captcha code:')
    return captcha_code
while True :
    x=input('Enter the DL-NO:')
    x=x.upper()
    y=input('Enter the DOB:')
    y=y.replace('/','-')
    r = requests.get(url=url)
    cookies = r.cookies
    tree=html.fromstring(r.content)
    auth = tree.xpath('//input[@name="javax.faces.ViewState"]/@value')
    z=auth[0]
    data = {
              'javax.faces.partial.ajax': 'true',
              'javax.faces.source': 'form_rcdl:j_idt46',
              'javax.faces.partial.execute': '@all',
              'javax.faces.partial.render': 'form_rcdl:pnl_show form_rcdl:pg_show form_rcdl:rcdl_pnl',
              'form_rcdl:j_idt46': 'form_rcdl:j_idt46',
              'form_rcdl': 'form_rcdl',
              'form_rcdl:tf_dlNO': x,
              'form_rcdl:tf_dob_input':y,
              'javax.faces.ViewState':z,
              'form_rcdl:j_idt34:CaptchaID':get_captcha()
    }
    r = requests.post(url=url, data=data, cookies=cookies)

    tree=html.fromstring(r.content)
    a=tree.xpath('//table[@class="table table-responsive table-striped table-condensed table-bordered"]/tr/td[1]//text()')
    if a !=[ ]:
        break
    print('WRONG DETAILS TRY AGAIN!')
a2=tree.xpath('//table[@class="table table-responsive table-striped table-condensed table-bordered"]/tr/td[2]//text()')
t1={ }
for i in range(len(a)):
    t1[a[i]]=a2[i]
b1=tree.xpath('//table[@class="table table-responsive table-striped table-condensed table-bordered data-table"]/tr/td//text()')
t2={
    b1[0]:{b1[1]:b1[2],b1[3]:b1[4]},
    b1[5]:{b1[6]:b1[7],b1[8]:b1[9]},
    b1[10]:b1[11],
    b1[12]:b1[13]
   } 
c=tree.xpath('//tbody/tr/td/text()')   
d=tree.xpath('//tr/th/span/text()')
i=0
j=1
t3={ }
while i<len(c):
        t3[j]={d[0]:c[i],d[1]:c[i+1],d[2]:c[i+2]}
        i=i+3
        j=j+1

t4={'Persontal Information':t1,'Driving License Validity':t2,'Class Of Vehicle Details':t3}

pos=json.dumps(t4,indent=3)
print(pos)
