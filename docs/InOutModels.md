<p>
<p>

# Input and output dimensions for multidimensional models.


In the table we show the shapes of the input arrays and return 
arrays for the methods result(), partal() and derivative(), 
for models with more dimensional inputs or outputs.

<p>
mdl-1-1 : a model with 1 dim inputs and 1 dim outputs<br>
mdl-I-1 : a model with I dim inputs and 1 dim outputs<br>
mdl-1-O : a model with 1 dim inputs and O dim outputs<br>
mdl-I-O : a model with I dim inputs and O dim outputs<br>
<p>

| array   | mdl-1-1 | mdl-I-1 | mdl-1-O  | mdl-I-O  | 
|:-------:|:-------:|:-------:|:--------:|:--------:|
| ndata   |     N   |    N    |    N     |    N     |
| npars   |     P   |    P    |    P     |    P     |
| ndim    |     -   |    I    |    -     |    I     |
| ndout   |     -   |    -    |    O     |    O     |
|**method** |       |         |          |          |
| input   |   (N)   |  (N,I)  |   (N)    |  (N,I)   |
| result  |   (N)   |   (N)   |  (N,O)   |  (N,O)   |
| partial |  (N,P)  |  (N,P)  | (O)(N,P) | (O)(N,P) |
|  (dfdp) |         |         |          |          |
| derivative|   (N)   |  (N,I)  |  (N,O)   | (O)(N,I) |
|  (dfdx) |         |         |          |          |


