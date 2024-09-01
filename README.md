# N-Queens Solver Project

<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg" alt="Python Logo" width="150">
</p>

## Integrantes do Grupo

- Rafael
- Gustavo
- Igor
- Eduardo
- Giovani
- Davi
- Steiger

## Descrição do Trabalho

Este projeto foi desenvolvido como parte da disciplina **Sistemas Distribuídos** na Universidade Tecnológica Federal do Paraná. O objetivo do trabalho foi resolver o problema das *N Rainhas* utilizando abordagens sequenciais e paralelas, implementadas em Python.

A solução envolve duas versões do algoritmo de backtracking:

- **Não Otimizado:** Uma implementação básica do algoritmo de backtracking.
- **Otimizado com Branch and Bound:** Uma versão otimizada que utiliza a técnica de *Branch and Bound* para reduzir o espaço de busca.

Além disso, implementamos versões paralelas de ambos os algoritmos, utilizando threads para distribuir o trabalho e acelerar o processo de solução.

## Tecnologia Utilizada

O projeto foi desenvolvido em **Python**, utilizando a biblioteca **DearPyGui** para a construção de uma interface gráfica que compara visualmente os tempos de execução das diferentes abordagens.

```bash
Python 3.9+
DearPyGui 1.7+
Threads para paralelismo
