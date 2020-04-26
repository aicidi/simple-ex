//use std::io;
//
//fn main() {
//    println!("Input");
//
//    let mut numbers = String::new();
//
//    io::stdin().read_line(&mut numbers)
//        .expect("Failed to read line");
//    let numbers = numbers.trim();
//
//    let tokens: Vec<&str> = numbers.split(" ").collect();
//
//    let a = tokens[0].parse::<i32>().unwrap();
//    let calc = tokens[1];
//    let b = tokens[2].parse::<i32>().unwrap();
//
//    let result = match calc {
//        "+" => a + b,
//        "-" => a - b,
//        "*" => a * b,
//        "/" => a / b,
//        _ => 1
//    };
//
//    println!("result {}", result);
//}

extern crate reqwest;
extern crate select;

use select::document::Document;
use select::predicate::Class;
use std::io::Read;
use std::collections::HashMap;
use std::hash::Hash;
use std::sync::{Mutex, Arc};
use std::thread;


#[derive(PartialEq, Eq, PartialOrd, Ord, Hash, Debug)]
struct User {
    nick: String,
    ip: String,
    uid: String,
}

impl User {
    pub fn new(nick: &str, ip: &str, uid: &str) -> Self {
        User { nick: String::from(nick), ip: String::from(ip), uid: String::from(uid) }
    }
}

fn cnt_user(user_map: &mut HashMap<User, i64>, user: User) {
    if user_map.contains_key(&user) {
        *user_map.get_mut(&user).unwrap() += 1;
    } else {
        user_map.insert(user, 1);
    }
}

fn get_page(url: &str, mut signed_map: &mut HashMap<User, i64>, mut unsigned_map: &mut HashMap<User, i64>)
            -> Result<(), Box<dyn std::error::Error>> {
    let mut res = reqwest::blocking::get(url)?;
    let mut body = String::new();
    res.read_to_string(&mut body)?;

    let document = Document::from(body.as_str());
    let mut content = document.find(Class("ub-content"));

    content.next();
    for node in content {
        let writer = node.find(Class("gall_writer")).next().unwrap();

        let nick = writer.attr("data-nick").unwrap();
        let ip = writer.attr("data-ip").unwrap();
        let uid = writer.attr("data-uid").unwrap();

        let user = User::new(nick, ip, uid);

        if ip == "" {
            cnt_user(&mut signed_map, user);
        } else if uid == "" {
            cnt_user(&mut unsigned_map, user);
        }
    }

    Ok(())
}

fn main() {
    let signed_map: HashMap<User, i64> = HashMap::new();
    let unsigned_map: HashMap<User, i64> = HashMap::new();

    let mut sign_mutex = Arc::new(Mutex::new(signed_map));
    let mut unsign_mutex = Arc::new(Mutex::new(unsigned_map));

    let mut handles = vec![];

    for i in 0..50 {
        let m1 = Arc::clone(&mut sign_mutex);
        let m2 = Arc::clone(&mut unsign_mutex);

        let handle = thread::spawn(move || {
            let url = format!("https://gall.dcinside.com/mgallery/board/lists/?id=github&page={}", i);
            let _ = get_page(url.as_str(), &mut m1.lock().unwrap(),
                             &mut m2.lock().unwrap());
        });

        handles.push(handle);
    }

    for handle in handles {
        handle.join().unwrap();
    }

    let sm = sign_mutex.lock().unwrap();
    let usm = unsign_mutex.lock().unwrap();

    let sm_vec: Vec<_> = sm.iter().collect();
    let usm_vec: Vec<_> = usm.iter().collect();

    let mut concat_vec: Vec<_> = [&sm_vec[..], &usm_vec[..]].concat();
    concat_vec.sort_by(|x, y| y.1.cmp(x.1));

    for (user, cnt) in concat_vec.iter() {
        println!("{:?} key {}", user, cnt);
    }
}
