# Álgebra relacional

## Pergunta 1

$$
\text{high\_replanished\_products\_from\_instant} \leftarrow \pi_{\text{ean, units}}(\sigma_{\text{instant > "2021/12/31 23:59" and }}\sigma_{\text{units > 10}}\text{(Replenishment\_event)})
$$ 

$$
\text{products\_with\_description} \leftarrow \pi_{\text{ean, descr}}(\text{Product} \bowtie \text{high\_replanished\_products\_from\_instant}) 
$$

$$
\text{desired\_products} \leftarrow \pi_{\text{ean, descr}} (\sigma_{\text{name = "Barras Energéticas"}}(\text{products\_with\_description} \bowtie \text{has}))
$$




## Pergunta 2

$$
\text{desired\_products} \leftarrow \pi_{\text{serial\_number}}( \sigma_{\text{ean = "9002490100070"}} (\text{planogram}) )
$$


## Pergunta 3

$$
\text{sub\_category\_count} \leftarrow \rho_{\text{count()}\mapsto\text{sub\_categ\_count}}(G_{\text{count()}}( \sigma_{\text{super\_category\_name = 'Sopas Take-Away'}} (\text{has\_other})))
$$


## Pergunta 4

$$
\text{replenished\_units\_ean} \leftarrow _{\text{ean}}G_{\text{sum(units)}} (\text{Replenishment\_event})  
$$
 
$$
\text{products\_with\_units} \leftarrow (\text{replenished\_units\_ean} \bowtie \text{Product})
$$

$$
\text{products\_with\_units2} \leftarrow \rho_{\text{sum(units)}\mapsto\text{units2, }\text{ean}\mapsto\text{ean2, }\text{descr}\mapsto\text{descr2}}
$$


$$ 
\text{max\_product} \leftarrow ( \pi_{\text{ean, descr}}(\text{products\_with\_units}) - \pi_{\text{ean, descr}} (\text{products\_with\_units} \bowtie_{\text{sum(units)}<\text{units2}} \text{product\_with\_units2} ) )
$$