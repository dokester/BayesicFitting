<p>
<p>

# Input and output dimensions for multidimensional models.


In the table we show the shapes of the input arrays and results 
for models with more dimensional inputs or outputs 

<p>
mdl-1-1 : a model with 1 dim inputs and 1 dim outputs<br>
mdl-*-1 : a model with n dim inputs and 1 dim outputs<br>
mdl-1-* : a model with 1 dim inputs and k dim outputs<br>
mdl-*-* : a model with n dim inputs and k dim outputs<br>
<p>

| array   | mdl-1-1 | mdl-*-1 | mdl-1-*  | mdl-*-*  | 
|:-------:|:-------:|:-------:|:--------:|:--------:|
| ndata   |     N   |    N    |    N     |    N     |
| npars   |     P   |    P    |    P     |    P     |
| ndim    |     -   |    I    |    -     |    I     |
| ndout   |     -   |    -    |    O     |    O     |
|:-------:|:-------:|:-------:|:--------:|:--------:|
| input   |   [N]   |  [N,I]  |   [N]    |  [N,I]   |
| result  |   [N]   |   [N]   |  [N,O]   |  [N,O]   |
| partial |  [N,P]  |  [N,P]  | [O][N,P] | [O][N,P] |
|  (dfdp) |         |         |          |          |
| deriv   |   [N]   |  [N,I]  |  [N,O]   | [O][N,I] |
|  (dfdx) |         |         |          |          |
|:-------:|:-------:|:-------:|:--------:|:--------:|

