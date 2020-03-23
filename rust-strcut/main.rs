struct Foo {
    cnt: i32,
}

impl Foo {
    fn make_foo() -> Foo {
        Foo { cnt: 0 }
    }
}

struct Bar {
    foo: Option<Foo>,
}

impl Bar {
    fn set_foo(&mut self, foo: Foo) {
        self.foo = Some(foo);
    }
}

fn add(foo: &mut Foo) {
    foo.cnt += 1;
}

fn main() {
    let mut foo = Foo::make_foo();
    add(&mut foo);

    println!("Foo cnt: {}", foo.cnt);

    let mut bar = Bar { foo: None };
    bar.set_foo(foo);

    println!("Bar Foo cnt: {}", bar.foo.as_ref().unwrap().cnt);

    match &mut bar.foo {
        Some(f) => {
            add(f);
        }
        _ => {}
    }

    println!("Bar Foo cnt: {}", bar.foo.as_ref().unwrap().cnt);
}
