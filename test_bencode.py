from bencode import bdecode

dict = bdecode('d8:completei13e10:incompletei0e8:intervali1800e5:peers12:\x98\x88N"\x1a\xe2\x98\x88N"\x1a\xe1e')
print(dict)
