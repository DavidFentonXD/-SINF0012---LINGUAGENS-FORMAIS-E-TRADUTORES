function comparaTipos(a: number, b: string): boolean {
    return a > b;
}

function retornoErrado(x: number): number {
    let mensagem: string = "oi";
    if (x) {
        return mensagem;
    }
    return x;
}

function chamadaErrada(): number {
    return comparaTipos(1, 2, 3);
}
