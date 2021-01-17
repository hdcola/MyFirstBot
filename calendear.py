from icalevents.icalevents import events

url = "webcal://p72-caldav.icloud.com/published/2/NDE3OTkzMjk0NDE3OTkzMpSxb7ERH6yybgSlRn2nfyB4Hv7q5lfiDR7Fdx2tj3PeCWqnHVbkdy36ExtEYZ7PMeviqrlOuICN0CTECfxfDcw"
es = events(url,fix_apple=True)
for e in es:
    print(e)