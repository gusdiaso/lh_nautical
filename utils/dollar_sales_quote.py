import requests
from datetime import timedelta, datetime

def get_cambio(data):
    """Busca a média da cotação de venda do dólar para uma data."""
    data_fmt = data.strftime('%m-%d-%Y')  # formato MM-DD-AAAA exigido pela API
    
    url = (
        f"https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
        f"CotacaoDolarDia(dataCotacao=@dataCotacao)?"
        f"@dataCotacao='{data_fmt}'"
        f"&$format=json"
        f"&$select=cotacaoVenda"
    )
    
    try:
        response = requests.get(url)
        values = response.json().get('value', [])
        
        if values:
            # Média de todas as cotações de venda do dia
            media = sum(value['cotacaoVenda'] for value in values) / len(values)
            return media
            
    except Exception as e:
        print(f"Erro ao buscar câmbio para {data_fmt}: {e}")
    
    return None


def get_cambio_util(data):
    """Se não achar câmbio (feriado/fim de semana), busca o dia útil anterior."""
    for i in range(7):
        resultado = get_cambio(data - timedelta(days=i))
        if resultado:
            return resultado
    return None