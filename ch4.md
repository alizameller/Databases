02/06/24
# Relational Algebra
```
Sailors(sid: int, snarne: string, rating: int, age: real) 
Boats(bid: int, bnarne: string, coloT: string)
Reserves(sid: int, bid: int, day: date)
```

σ is Selection
- example: σ<sub>ratings > 8</sub>(S)
  
∪ is OR

∩ is AND
- example: R ∩ S = R - (R - S)

\- is Set Difference

π is Projection
- example: π<sub>sname, age</sub>(S)

X is Cross Producr
  
⨝ is Join operator
 -  example: ⨝<sub>C</sub> S = σ<sub>C</sub> (R X S)

### Examples:
1. Relactional Math translated into SQL
   
    π<sub>sname, age</sub> (σ<sub>ratings > 8</sub>(S))
    ```
    SELECT sname, age FROM Sailors 
        WHERE ratings > 8
    ```
2. Set Difference
    ``` 
    R       S       R-S
    1.0     1.0     2.0
    2.0     2.2     3.1
    3.1
    ```
3. Cross Product R X S
   ```
   R    S   
   1    4
   2    5
   3

   Cross Product returns 
   (1, 4), (1, 5), (2, 4), (2, 5), (3, 4), (3, 5)
   ```
4. S ⨝<sub>S, Sid</sub> = <sub>R, Sid</sub>R
   

