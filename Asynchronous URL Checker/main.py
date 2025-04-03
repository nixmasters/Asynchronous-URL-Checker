import asyncio
import httpx
import json

async def provjeriUrl(client, url,method='GET',data=None,token=None):
    status = None
    time = None
    response = None
    headers = {}
    try:
        if token :
            #ako imamo token , u authorization dodajemo token
            headers={"Authorization":token}
        #pocetak mjerenja vremena
        start_time = asyncio.get_event_loop().time()
        if(method=='GET' ):
            # ako ucitavanje sajta predje 2 sekunde dolazi do TimeoutException-a
            # ako je sajt premjesten follow_redirects redirektuje na pravi sajt
            response = await client.get(url, timeout=2, follow_redirects=True,headers=headers)
        elif(method=='POST'):
            response = await client.post(url,data=data, timeout=2, follow_redirects=True,headers=headers)
        #provjera za status servera
        response.raise_for_status()
        #kraj mjerenja vremena
        end_time = asyncio.get_event_loop().time()-start_time
        #zaokruzujem na tri decimale
        time = round(end_time,3)

        status = response.status_code
    except httpx.RequestError as e:
        #Mrezna greska ili problem do servera
        print(url + " error: Request Error")
        return {"url": url, "status_code": None, "response_time": None,"method":method, "error": f"Request Error: {e}"}

    except httpx.HTTPStatusError as e:
        #Greska statusa koda
        print(url + " error: HTTP Status Error ")
        return {"url": url, "status_code": e.response.status_code, "response_time": None,
                "method":method,"error": f"HTTP Status Error: {e}"}

    except httpx.TimeoutException:
        #Timeout greska
        print(url +" error: Timeout Error")
        return {"url": url, "status_code": None, "response_time": None,"method":method,
                "error": "Timeout Error"}

    return {
        #vracam url , statusni kod sajta i vrijeme odgovora sajta
        "url": url,
        "status_code": status,
        "response_time": time,
        "method" : method
    }

async def main():
    data = None
    #bypass za SSL verify na False
    async with httpx.AsyncClient(verify=False) as client:
        #otvaram urls.txt i citam liniju po liniju
        with open('urls.txt','r') as urls:
            tasks =[]
            for url in urls:
                parts = url.strip().split(maxsplit=2)
                method = parts[0]
                url = parts[1]
                token = parts[2] if len(parts) > 2 else None

                #dodajem requestove u listu taskova
                if(method=='GET' ):
                    tasks.append(provjeriUrl(client,url,method='GET',token=token))
                elif(method=='POST' ):
                    tasks.append(provjeriUrl(client, url, method='POST',data=data,token=token))
            #pokrecem sve requestove asinhrono i stavljam ih u rezultate
            rezultati = await asyncio.gather(*tasks)

    #pravim rezultati.json sa rezultatima prethodno dobijenim
    with open('rezultati.json','w') as json_file:
        #upisujem u json fajl sa nazivom rezultati.json sa indentom 4 za ljepsi ispis
        json.dump(rezultati,json_file,indent=4)


asyncio.run(main())



