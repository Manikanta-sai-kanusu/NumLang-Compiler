num a;
num b;
text msg;

a = 4;
b = a * 3;

msg = "Result is:";

show msg;
show b;

cond (b > 10) {
    show b;
}

loop (a < 10) {
    show a;
    a = a + 1;
}