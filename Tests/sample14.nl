func fact(num n) {
    cond (n == 0) {
        return 1;
    }
    return n * fact(n - 1);
}

num result;
result = fact(5);
show result;