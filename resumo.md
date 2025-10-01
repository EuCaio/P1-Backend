## 1. @staticmethod

O decorador `@staticmethod` é utilizado em Python para definir um método estático dentro de uma classe. Um método estático pertence a classe, e não a uma instância específica da classe. Isso significa que ele pode ser chamado diretamente a partir da classe, sem a necessidade de criar um objeto. A principal característica de um método estático é que ele não recebe uma referência implícita a instância (chamada de `self`) ou a classe (chamada de `cls`).

### Propósito e Uso

Métodos estáticos são úteis para agrupar funções de utilidade que têm uma conexão lógica com a classe, mas que não dependem do estado de nenhuma instância. Eles são essencialmente funções normais que estão aninhadas no namespace da classe. Isso ajuda a organizar o código e a manter a coesão, agrupando funcionalidades relacionadas. Por exemplo, uma classe que lida com conversões de unidades de medida pode ter métodos estáticos para realizar os cálculos de conversão, pois esses cálculos não dependem de nenhuma instância específica da classe.

### Exemplo Prático

```python
class ConversorTemperatura:
    @staticmethod
    def celsius_para_fahrenheit(celsius):
        return (celsius * 9/5) + 32

    @staticmethod
    def fahrenheit_para_celsius(fahrenheit):
        return (fahrenheit - 32) * 5/9

# Chamando os métodos estáticos diretamente da classe
fahrenheit = ConversorTemperatura.celsius_para_fahrenheit(25)
print(f"25°C em Fahrenheit é: {fahrenheit}°F")

celsius = ConversorTemperatura.fahrenheit_para_celsius(77)
print(f"77°F em Celsius é: {celsius}°C")
```

Neste exemplo, os métodos `celsius_para_fahrenheit` e `fahrenheit_para_celsius` são estáticos porque suas operações não dependem de nenhuma instância da classe `ConversorTemperatura`. Eles simplesmente recebem um valor de entrada e retornam um valor de saída, tornando-os candidatos ideais para serem métodos estáticos.

## 2. Dataclasses

As `Dataclasses` são um recurso que utiliza o decorador `@dataclass` para automatizar a geração de métodos especiais em classes que são usadas principalmente para armazenar dados. Métodos como `__init__()`, `__repr__()`, `__eq__()` e outros são adicionados automaticamente, o que reduz significativamente a quantidade de código repetitivo e torna as classes mais limpas e legíveis.

### Propósito e Uso

O principal propósito das `Dataclasses` é simplificar a criação de classes que servem como contêineres de dados. Antes das `Dataclasses`, a criação de uma classe para armazenar alguns atributos exigia a implementação manual do construtor (`__init__`) para atribuir os valores, do método `__repr__` para uma representação legível, e de métodos de comparação como `__eq__`. Com o decorador `@dataclass`, tudo isso é gerado automaticamente com base nas anotações de tipo dos atributos da classe.

### Exemplo Prático

```python
from dataclasses import dataclass

@dataclass
class Produto:
    id: int
    nome: str
    preco: float

# Criando uma instância da dataclass
produto1 = Produto(id=1, nome="Laptop", preco=3500.0)
produto2 = Produto(id=1, nome="Laptop", preco=3500.0)

# O __repr__ é gerado automaticamente
print(produto1)

# O __eq__ é gerado automaticamente
print(f"Os produtos são iguais? {produto1 == produto2}")
```

Neste exemplo, a classe `Produto` é decorada com `@dataclass`, o que instrui o Python a gerar automaticamente os métodos `__init__`, `__repr__`, e `__eq__`. Isso torna a classe concisa e focada em sua responsabilidade principal: armazenar dados sobre um produto.

## 3. Eventos de Domínio

Os **Eventos de Domínio** são um padrão de design, parte do **Domain-Driven Design (DDD)**, que representa algo significativo que aconteceu no domínio do negócio. Em vez de acoplar diretamente diferentes partes de um sistema, os eventos de domínio permitem uma comunicação desacoplada. Quando o estado de uma entidade ou agregado muda, um evento é disparado para notificar outras partes do sistema sobre essa mudança, sem que o emissor precise conhecer os receptores.

### Propósito e Uso

O principal propósito dos eventos de domínio é permitir a implementação de efeitos colaterais (side effects) de forma limpa e desacoplada. Por exemplo, quando um novo usuário se cadastra (`UsuarioCadastrado`), o sistema pode precisar enviar um e-mail de boas-vindas, criar um perfil inicial e notificar a equipe de vendas. Em vez de colocar toda essa lógica no mesmo lugar, o agregado `Usuario` simplesmente dispara o evento `UsuarioCadastrado`. Outros componentes, chamados de *manipuladores de eventos* (event handlers), escutam por esse evento e executam as ações apropriadas. Isso resulta em um sistema mais modular, manutenível e escalável.

### Exemplo Prático

```python
# Definição do evento (usando dataclass)
@dataclass(frozen=True)
class PedidoRealizado(DomainEvent):
    pedido_id: str
    cliente_id: str
    valor_total: float

# Na entidade Pedido
class Pedido:
    def __init__(self, cliente_id: str, valor_total: float):
        self.id = str(uuid.uuid4())
        self.cliente_id = cliente_id
        self.valor_total = valor_total
        self._domain_events = []
        self._add_domain_event(PedidoRealizado(
            pedido_id=self.id,
            cliente_id=self.cliente_id,
            valor_total=self.valor_total
        ))

    def _add_domain_event(self, event: DomainEvent):
        self._domain_events.append(event)

# Manipulador de evento
def enviar_email_confirmacao(event: PedidoRealizado):
    print(f"Enviando e-mail de confirmação para o pedido {event.pedido_id}...")

# Despachando o evento
dispatcher.register_handler(PedidoRealizado, enviar_email_confirmacao)

novo_pedido = Pedido(cliente_id="cliente-123", valor_total=199.90)
for event in novo_pedido.clear_domain_events():
    dispatcher.dispatch(event)
```

Neste exemplo, a criação de um `Pedido` dispara o evento `PedidoRealizado`. Um manipulador de eventos (`enviar_email_confirmacao`) é registrado para reagir a esse evento, mantendo a lógica de envio de e-mail separada da lógica de criação do pedido.

## 4. Decoradores

Em Python, um **decorador** é uma função que recebe outra função como argumento, adiciona alguma funcionalidade a ela e retorna uma nova função. Essencialmente, decoradores permitem modificar ou estender o comportamento de funções ou métodos sem alterar seu código-fonte original. Eles são uma forma elegante de aplicar padrões de design como o *Decorator Pattern* e são amplamente utilizados em frameworks web (como Flask e Django), para logging, medição de performance, controle de acesso, entre outros.

### Propósito e Uso

O principal propósito dos decoradores é adicionar funcionalidades transversais (cross-cutting concerns) a múltiplas funções de forma reutilizável e limpa. Em vez de copiar e colar o mesmo código em várias funções, um decorador encapsula essa lógica e a aplica onde for necessário. Isso promove a reutilização de código, melhora a legibilidade e facilita a manutenção, pois a lógica adicional pode ser alterada em um único local.

### Exemplo Prático

```python
def meu_decorador(func):
    def wrapper(*args, **kwargs):
        print("Antes da função ser chamada.")
        resultado = func(*args, **kwargs)
        print("Depois da função ser chamada.")
        return resultado
    return wrapper

@meu_decorador
def saudacao(nome):
    print(f"Olá, {nome}!")

saudacao("Mundo")
```

Neste exemplo, `meu_decorador` é uma função que atua como decorador. Ela recebe a função `saudacao` como argumento, envolve-a em uma função `wrapper` que adiciona mensagens antes e depois da execução da função original, e retorna essa `wrapper`. Ao usar `@meu_decorador` acima da definição de `saudacao`, estamos aplicando o decorador, e cada vez que `saudacao` é chamada, as mensagens "Antes da função ser chamada." e "Depois da função ser chamada." são exibidas.

## 5. Domain-Driven Design (DDD)

O **Domain-Driven Design (DDD)** é uma abordagem de desenvolvimento de software que coloca o **domínio** (a área de conhecimento e as regras de negócio) no centro do processo de design. O objetivo principal do DDD é alinhar o código com a linguagem e a lógica do negócio, criando um modelo de domínio rico que encapsula regras e comportamentos complexos. Isso resulta em sistemas mais expressivos, manuteníveis e que refletem com precisão a realidade do negócio.

### Propósito e Princípios

O DDD foca na compreensão profunda do domínio, promovendo uma colaboração intensa entre especialistas de domínio e desenvolvedores. Seus princípios incluem:

*   **Linguagem Ubíqua (Ubiquitous Language)**: Uma linguagem comum e consistente, compartilhada por todos os membros da equipe (técnicos e não-técnicos), que é refletida diretamente no código, testes e documentação. Isso elimina ambiguidades e garante que todos falem a mesma "língua" do negócio.
*   **Contextos Delimitados (Bounded Contexts)**: Define limites lógicos dentro de um sistema onde um modelo de domínio específico é válido e consistente. Dentro de um contexto delimitado, os termos da Linguagem Ubíqua têm um significado preciso, evitando confusões que poderiam surgir em sistemas maiores e mais complexos.

### Padrões Táticos do DDD

Para construir um modelo de domínio expressivo, o DDD utiliza diversos padrões táticos:

*   **Entidades (Entities)**: Objetos que possuem uma identidade única e contínua ao longo do tempo, independentemente de seus atributos. São identificados por um ID (ex: `Cliente`, `Produto`).
*   **Objetos de Valor (Value Objects)**: Objetos que são caracterizados apenas por seus atributos, são imutáveis e comparados por valor. Não possuem identidade própria (ex: `Endereco`, `Dinheiro`).
*   **Agregados (Aggregates)**: Um cluster de Entidades e Objetos de Valor que são tratados como uma única unidade transacional. Possuem uma **Raiz do Agregado (Aggregate Root)** que garante a consistência interna do agregado e é o único ponto de acesso externo.
*   **Serviços de Domínio (Domain Services)**: Lógica de negócio que não se encaixa naturalmente em Entidades ou Objetos de Valor. São operações stateless que orquestram ações complexas envolvendo múltiplos objetos de domínio.
*   **Repositórios (Repositories)**: Fornecem uma camada de abstração para a persistência de dados, permitindo que o domínio acesse e salve agregados sem se preocupar com os detalhes da tecnologia de armazenamento.
*   **Fábricas (Factories)**: Encapsulam a lógica de criação de objetos complexos (Entidades e Agregados), garantindo que os objetos sejam criados em um estado válido.

### Arquitetura e Camadas

O DDD promove uma arquitetura em camadas que separa as preocupações, geralmente incluindo:

*   **Camada de Domínio (Domain Layer)**: O coração do sistema, contendo as regras de negócio, entidades, objetos de valor, agregados e serviços de domínio. Não deve ter dependências de infraestrutura.
*   **Camada de Aplicação (Application Layer)**: Orquestra as operações do domínio, traduzindo requisições externas em comandos de domínio. Não contém regras de negócio.
*   **Camada de Infraestrutura (Infrastructure Layer)**: Lida com detalhes técnicos como persistência de dados, comunicação externa (APIs, mensageria) e outros serviços técnicos.
*   **Camada de Apresentação (Presentation Layer)**: Responsável pela interface com o usuário (UI) ou por expor uma API (como uma API REST).

O DDD é fundamental para construir sistemas complexos que são fáceis de entender, modificar e expandir, mantendo uma forte ligação com o negócio que representam.

