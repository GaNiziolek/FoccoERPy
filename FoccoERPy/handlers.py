import json
from benedict import benedict

def handle_json(json_dict) -> dict:
    """
        Os retornos da API do FoccoERP organiza os dados no JSON utilizando
        um esquema de organização diferente do usual.
        Cada parte do JSON possui um atributo "$id", que pode ser referenciado
        em outras partes do mesmo JSON que devam conter exatamente o mesmo valor,
        essa referencia é feita por meio do atributo "$ref".

        Apesar de esse esquema diminui o tamanho do JSON, é necessário tratar esse JSON
        e reverter esse tratamento.

        Essa função realiza essa conversão.
    """
    _data = json_dict

    values=[_data]

    i = 0
    # Inicialmente "values" contem somente o json completo recebido,
    # é feito uma busca por todas as chaves que tambem possuem filhos
    # e quando encontrados, serao adicionadas na lsita "values",
    # dessa forma cada parte do json será encontrada, desmembrada e 
    # armazenada na lista "values"
    for val in values:
        
        # Para cada chave do json
        for k, v in val.items():

            # Se a chave ja nao estiver adicionada na lista
            if not v in values:
                
                # Se a chave for um json (tipo dict em python)
                if isinstance(v, dict):
                    values.append(v)
                    #print(f'appended: "{k}", id: "{v.get("$id", "")}", ref: "{v.get("$ref", "")}", list size {len(values)}')

                # Se for uma lista, itera entre os elementos dessa lista
                elif isinstance(v, list):
                    for count, e in enumerate(v):
                        if isinstance(e, dict):
                            values.append(e)
                            #print(f'appended: "{count}-{k}", id: "{e.get("$id", "")}", ref: "{e.get("$ref", "")}", list size {len(values)}')

        # Nao realiza mais que 1000 iteracoes, para evitar que algum erro nao previsto
        # possa gerar um codigo em loop que nunca ira finalizar
        i += 1
        if i >= 1000:
            break
    
    ids  = []
    refs = []

    for v in values:
        if '$id' in v.keys():
            ids.append(v)
        elif '$ref' in v.keys():
            refs.append(v)

    _json = json.dumps(_data)

    for ref in refs:
        #print(f'ref: {ref.get("$ref")}')
        if json.dumps(ref) in _json:
            for id in ids:
                #print(f'id: {id.get("$id")}')
                if id.get('$id') == ref.get('$ref'):
                    #print(f'id: {id.get("$id")} = ref: {ref.get("$ref")}')
                    _json = _json.replace(json.dumps(ref), json.dumps(id))

    return benedict(json.loads(_json))