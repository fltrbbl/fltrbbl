# fltrbbl


    cd dummy_client
    python client.py put user -d '{"email": "testemail@abc.de", "password": "testpassword"}'
    python client.py put feeds -d '{"url": "https://www.heise.de/newsticker/heise-atom.xml"}'
    #wait for the feedupdate
    python client.py get feed
    python client.py get vectors