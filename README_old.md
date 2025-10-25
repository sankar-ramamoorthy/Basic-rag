2025/10/15.
at this point i am able to 
invoke the generate endpoint in llm-service, supply a context nd user query and have the llm reply to that (ollama , model Qwen3:1.7b)

PS C:\Users\bosto\dockerstuff\Basic-rag> Test-NetConnection -ComputerName localhost -Port 8003


ComputerName     : localhost
RemoteAddress    : ::1
RemotePort       : 8003
InterfaceAlias   : Loopback Pseudo-Interface 1
SourceAddress    : ::1
TcpTestSucceeded : True



PS C:\Users\bosto\dockerstuff\Basic-rag> $body = @{ context = "daisy lived in A colorful home in what used to be calcutta in India"; query = "Where was daisy's home?" } | ConvertTo-Json
PS C:\Users\bosto\dockerstuff\Basic-rag> Invoke-RestMethod -Uri "http://localhost:8003/generate?provider=ollama&model=Qwen3:1.7b" `
>>   -Method POST `
>>   -ContentType "application/json" `
>>   -Body $body

provider model      response
-------- -----      --------
ollama   Qwen3:1.7b Daisy's home was in **Calcutta, India**. ...

Arnab and I are also able to test the chunking method in the ingest-service.
curl http://localhost:8001/test-chunking 

curl http://localhost:8001/test-chunking


StatusCode        : 200
StatusDescription : OK
Content           : {"num_chunks":2,"sample":["This is a long paragraph of text. This is a long paragraph of text.
                    This is a long paragraph of text. This is a long paragraph of text. This is a long paragraph of
                    text. Thi...
RawContent        : HTTP/1.1 200 OK
                    Content-Length: 1944
                    Content-Type: application/json
                    Date: Thu, 16 Oct 2025 03:30:18 GMT
                    Server: uvicorn

                    {"num_chunks":2,"sample":["This is a long paragraph of text. This is a lo...
Forms             : {}
Headers           : {[Content-Length, 1944], [Content-Type, application/json], [Date, Thu, 16 Oct 2025 03:30:18 GMT],
                    [Server, uvicorn]}
Images            : {}
InputFields       : {}
Links             : {}
ParsedHtml        : System.__ComObject
RawContentLength  : 1944



PS C:\Users\bosto\dockerstuff\Basic-rag>

PS C:\Users\bosto\dockerstuff\Basic-rag>
