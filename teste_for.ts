function testeFor(n: number): number {
    let soma: number = 0;
    for (let i: number = 0; i < n; i = i + 1) {
        soma = soma + i;
    }
    return soma;
}
