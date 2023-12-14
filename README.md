# Bot de Scrapping de Clientes

Este é um script Python que utiliza a Google Maps API para buscar estabelecimentos com base em um tipo de estabelecimento usando localizações pré-definidas.

## Configuração

### Requisitos

- Python 3.x
- API KEY do Google Maps

### Instalação

```
pip install -r requirements.txt
```

Certifique-se de criar um `.env` na raiz do projeto e adicionar sua chave google assim:

```
API_KEY=CHAVE_AQUI
```

### Utilização

- Execute o script main.py.
- Será solicitado que você digite o tipo de estabelecimento que deseja pesquisar.
- O script buscará esse tipo de estabelecimento em várias cidades do Brasil.
- Os resultados serão armazenados em um arquivo Excel com o formato <tipo-de-estabelecimento>_clientes.xlsx.


### Observações
- Este script faz uso de várias localizações pré-definidas no Brasil para buscar os estabelecimentos desejados.
- Há um intervalo de espera de 2 segundos entre as solicitações à API para respeitar as limitações impostas pela Google.
- O arquivo Excel gerado conterá informações como nome, website, endereço e telefone dos estabelecimentos encontrados, quando disponíveis.
- 
### Contribuição
Se quiser contribuir para este projeto, sinta-se à vontade para abrir issues ou pull requests =)
