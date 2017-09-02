import socket,json,textwrap

print("Servidor HTTP")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('127.0.0.1', 9100))
s.listen(1)

while True:
    client_connection, client_address = s.accept()
    request = client_connection.recv(1024)

    string_request = request.decode('utf-8')

    #array para json
    data = {}
    data['path'] = string_request.split(' ')[1]
    data['protocol'] = (string_request.split(' ')[2]).split('\r')[0]
    data['method'] = string_request.split(' ')[0]

    headers = string_request.split(data['protocol'],1)[1]

    headers_data = {}

    for line in headers.splitlines():
        if(len(line)>0):
            key = line.split(':')[0]
            value = line.split(':')[1]
            headers_data[key]=value

    json_headers = json.dumps(headers_data)

    data['headers'] = headers_data

    json_data = json.dumps(data)

    r_file = "documentRoot" + data['path']

    try:
        f = open(r_file,"rb")
        content = f.read()
        f.close()

        content = textwrap.dedent(content)

        header="HTTP/1.1 200 OK\n"


    #para mostrar 404 si no existe
    except Exception as e:
        content=""
        header="HTTP/1.1 404 Not Found\n"

    client_connection.sendall(header+ "X-RequestEcho: " + json_data + "\n" + content)
    client_connection.close()
