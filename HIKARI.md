# HIKARI - Plataforma de Competição Blue Team

HIKARI é uma plataforma de competição baseada no CTFd, focada em atividades de Blue Team. Os participantes se organizam em times e devem analisar logs de segurança para encontrar evidências de ataques.

### Como Funciona
- Os times resolvem desafios práticos relacionados à detecção e resposta a ameaças.
- Cada time tem acesso a um ambiente Kibana contendo logs de invasões simuladas.
- Novos logs são injetados conforme os desafios são resolvidos.
- Times que demoram mais para resolver desafios precisarão analisar um volume maior de logs.
- As flags podem ser IPs, URLs, nomes de arquivos maliciosos, entre outros indicadores de comprometimento.

### Objetivo
A plataforma busca simular cenários realistas de segurança cibernética, treinando os participantes na identificação e resposta a incidentes.

### Tecnologias Utilizadas
- [CTFd](https://github.com/CTFd/CTFd) como base para os desafios
- Kibana para visualização e análise de logs
- Injeção dinâmica de logs conforme a progressão dos times

### Como Participar
1. Forme um time e registre-se na plataforma.
2. Acesse o ambiente Kibana disponibilizado.
3. Resolva desafios analisando os logs para encontrar as flags.
4. Avance na competição e melhore suas habilidades de defesa cibernética!


## Como criar uma competição
    (!) Ao criar a competição, selecionar sempre o modo de times.
    (1) Todas as demais configurações podem ser customizadas.


## Criação de desafios
    (1) Acessar página de administrador.
    (2) Acessar página de desafios.
    (3) Selecionar o "+" para adicionar um desafio.
    (4) Selecionar tipo de desafio "HIKARI".
    (5) Adicionar o arquivo .json que corresponde aos logs necessários para resolver o desafio.
    (6) Customizar o restante do desafio conforme necessidade.
    (7) COMPLEMENTO: Na criação do desafio, há a opção de selecionar outros desafios como requisitos. Isso crie uma cadeia lógica de injeção de logs na plataforma KIBANA. Desse modo, se o desafio A depende do B, então assim que QUALQUER time finalizar o desafio B, os logs do A serão injetados.

## Gerenciamento da competição
    (1) Acessar página de administrador.
    (2) Acessar submenu "plugins".
    (3) Selecionar o plugin hikari.
    (4) Nesta etapa, a página de administração do projeto HIKARI estará disponível.
    (5) Basta clicar em "Iniciar Competição"
    (6) OBSERVAÇÃO: Os logs de todos os desafios marcados como VISÍVEIS na plataforma serão injetados, para que eles possam ser resolvidos pelos usuários.
    (7) A competição pode ser resetada. Quando isso ocorre, os logs serão injetados novamente quando o administrador clicar em "Iniciar Competição". ATENÇÃO: OS LOGS NÃO SÃO REMOVIDOS DO KIBANA.

---

HIKARI: Treine suas habilidades de defesa cibernética em um ambiente dinâmico e desafiador!






