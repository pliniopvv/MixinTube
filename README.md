### Estrutura dos arquivos

> \$ python repo.py roteiro.raw \
> \$ python montagem.py montagem.raw
> \$ python montagemconcat.py montagemconcat.raw

<details>
<summary>roteiro.raw</summary>
composição das linhas:
<pre>[arquivo_principal] [link] [início] [fim] [descriçao do corte]</pre>
</details>

<details>

<summary>montagem.raw</summary>
Composição do corte:
<pre>
concat [nome do corte]
[
    [descrição/nome do corte]
    [descrição/nome do corte]
        ...
]
concat:text [nome do arquivo]
[
    [descrição/nome do corte]|[Texto sobre o vídeo]
    [descrição/nome do corte]|[Texto sobre o vídeo]
        ...
]
midnight [nome do arquivo]
[
    [descrição/nome do corte]
    [descrição/nome do corte]
        ...
]
array [nome do corte]
[
    [descrição/nome do corte]
    [descrição/nome do corte]
        ...
]
</pre>
</details>

<details>
<summary>montagemconcat.raw</summary>
<pre>[descrição do corte]|[descrição do corte]|[descrição do corte]</pre>
</details>