element = {"nom": "iLiaisonVpnCNMP"}
var = "CNMP"

if var in element.get("nom"):
    print("CNMP est présent dans iLiaisonVpnCNMP")
else:
    print("CNMP n'est pas présent dans iLiaisonVpnCNMP")