# Multithreaded Web Server with Rust

Simple web server built using Rust. In this blog I will walk through the steps in building it, with heavy[^1] reference to [Chapter 20 of the Rust book](https://doc.rust-lang.org/beta/book/ch20-01-single-threaded.html).

[^1]: Heavy means a lot of text will be lifted from the Rust book and it is not my own words. I only attempt to summarize it as much as possible so that I can reference it in the future.

## Part 1: Building a single-threaded web server.

We will start off by building a simple single-threaded web server using Rust. Upon a successful connection, we will read the `GET` request sent by the web page and send a simple "Hello world" html page. For requests to all other pages, we will send a simple "404" page instead. Let's get started!

> #### Before we begin:
>
> Some useful background information on [TCP](https://en.wikipedia.org/wiki/Transmission_Control_Protocol)and [HTTP](https://www.cloudflare.com/learning/ddos/glossary/hypertext-transfer-protocol-http/) will be helpful. This blog also assume some basic knowledge of Rust.

### Listening to the TCP Connection

First and foremost, our web server will need to listen to a TCP connection. We can do this using the `std::net` module offered by Rust's standard library. In the code below, we create a `TcpListener` object and bind it to our local address `127.0.0.1:7878`. `127.0.0.1` is our local IP address (which is the same for every computer) and `7878` is the port. We can choose any port we want as long as we do not conflict with other ports running on the machine.

```rust
// Filename: src/main.rs
use std::net::TcpListener;

fn main() {
    let listener = TcpListener::bind("127.0.0.1:7878").unwrap();

    for stream in listener.incoming() {
        let stream = stream.unwrap();

        println!("Connection established!");
    }
}
```

If we run the code and navigate to `localhost:7878` on our browser, we will see `Connection established!` on our terminal. On the browser side, we will not see anything because our web server is not sending anything over yet.

### Reading the Request

Before we continue, try the following exercise yourself.

> **Exercise**
>
> Implement the function `fn handle_connection(mut stream: TcpStream)` that will read the data from the TcpStream object and print the HTTP request sent to our web server from it.

Your code should look like this:

```rust
// Filename: src/main.rs
use std::{
    io::{prelude::*, BufReader},
    net::{TcpListener, TcpStream},
};

fn main() {
    let listener = TcpListener::bind("127.0.0.1:7878").unwrap();

    for stream in listener.incoming() {
        let stream = stream.unwrap();

        handle_connection(stream);
    }
}

fn handle_connection(mut stream: TcpStream) {
    let buf_reader = BufReader::new(&mut stream);
    let http_request: Vec<_> = buf_reader
        .lines()
        .map(|result| result.unwrap())
        .take_while(|line| !line.is_empty())
        .collect();

    println!("Request: {http_request:#?}");
}
```

In the `handle_connection` function, we create a new `BufReader` instance that wraps a mutable reference to the stream. `BufReader` adds buffering by managing calls to the `std::io::Read` trait methods for us.

The browser signals the end of an HTTP request by sending two newline characters in a row. To get one request from the stream, we take lines until we get a line that is the empty string.

Let's start the program and make a request in the web browser again. We will still see the error page in the browser, but now our terminal should print something like this:

```sh
$ cargo run
   Compiling hello v0.1.0 (file:///projects/hello)
    Finished dev [unoptimized + debuginfo] target(s) in 0.42s
     Running `target/debug/hello`
Request: [
    "GET / HTTP/1.1",
    "Host: 127.0.0.1:7878",
    "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:99.0) Gecko/20100101 Firefox/99.0",
    "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language: en-US,en;q=0.5",
    "Accept-Encoding: gzip, deflate, br",
    "DNT: 1",
    "Connection: keep-alive",
    "Upgrade-Insecure-Requests: 1",
    "Sec-Fetch-Dest: document",
    "Sec-Fetch-Mode: navigate",
    "Sec-Fetch-Site: none",
    "Sec-Fetch-User: ?1",
    "Cache-Control: max-age=0",
]
```

### Analyzing the HTTP Request

HTTP is a text-based protocol, and a request takes this format:

```plaintext
Method Request-URI HTTP-Version CRLF
headers CRLF
message-body
```

The first line is the _request line_ that holds information about what the client (our web browser) is requesting. The first part of the request line indicates the _method_ being used, such as `GET` or `POST`, which describes how the client is making this request. Our client used a `GET` request, which means it is asking for information.

The next part of the request line is `/`, which indicates the _Uniform Resource Identifier (URI)_ the client is requesting (NOT the same as Uniform Resource Locator (URL)).

The last part is the HTTP version the client uses, and then the request line ends in a `CRLF` sequence (`\r\n`). The CRLF sequence separates the request line from the rest of the request data. Note that when the CRLF is printed, we see a new line start rather than `\r\n`.

Looking at the request line data we received from running our program so far, we see that `GET` is the method, `/` is the request URI, and `HTTP/1.1` is the version.

After the request line, the remaining lines starting from `Host:` onward are headers. `GET` requests have no body.

### Writing a Response.

We’re going to implement sending data in response to a client request. Responses have the following format:

```plaintext
HTTP-Version Status-Code Reason-Phrase CRLF
headers CRLF
message-body
```

The first line is a _status line_ that contains the HTTP version used in the response, a numeric status code that summarizes the result of the request, and a reason phrase that provides a text description of the status code. After the CRLF sequence are any headers, another CRLF sequence, and the body of the response.

Here is an example response that uses HTTP version 1.1, has a status code of 200, an OK reason phrase, no headers, and no body:

```plaintext
HTTP/1.1 200 OK\r\n\r\n
```

The status code 200 is the standard success response. The text is a tiny successful HTTP response.

Let's modify the `handle_connection` function to send a response back to the browser.

```rust
// Filename: src/main.rs
fn handle_connection(mut stream: TcpStream) {
    let buf_reader = BufReader::new(&mut stream);
    let http_request: Vec<_> = buf_reader
        .lines()
        .map(|result| result.unwrap())
        .take_while(|line| !line.is_empty())
        .collect();

    let response = "HTTP/1.1 200 OK\r\n\r\n";

    stream.write_all(response.as_bytes()).unwrap();
}
```

> Note that the `write_all` method can fail, and we will be adding error handling there in the real world. But in this case I am just trying to get my server up and running fast 🏃.

With these changes, let's run our code again and make a request. This time, we see a blank page instead of an error. Yay!

### Returning a Real HTML Page

Let's try to return a simple HTML page. Here is another simple exercise!

> **Exercise**
>
> Modify `handle_connection` to return a simple HTML page (such as `index.html`).
>
> Hint 1: Refer to the section on [Writing a Response](#writing-a-response) on how the response should look like.
>
> Hint 2: You will need to read the contents in `index.html` into a string. You can use `fs::read_to_string` to help you with that.

Our code should look like this:

```rust
// Filename: src/main.rs
use std::{
    fs,
    io::{prelude::*, BufReader},
    net::{TcpListener, TcpStream},
};
// --snip--

fn handle_connection(mut stream: TcpStream) {
    let buf_reader = BufReader::new(&mut stream);
    let http_request: Vec<_> = buf_reader
        .lines()
        .map(|result| result.unwrap())
        .take_while(|line| !line.is_empty())
        .collect();

    let status_line = "HTTP/1.1 200 OK";
    let contents = fs::read_to_string("hello.html").unwrap();
    let length = contents.len();

    let response =
        format!("{status_line}\r\nContent-Length: {length}\r\n\r\n{contents}");

    stream.write_all(response.as_bytes()).unwrap();
}
```

Run the code, and refresh your browser. You will see your HTML rendered!

Currently, we are ignoring the request data in `http_request` and sending back `index.html` unconditionally. So if we load _127.0.0.1/something-else_, we will still see the exact same HTML response. We want to customize our responses depending on the request that is sent to our server and only send back the HTML file for a well-formed request to `/`.

### Validating the Request and Selectively Responding

Right now, our web server will return the HTML in the file no matter what the client requested. Let’s add functionality to check that the browser is requesting / before returning the HTML file and return an error if the browser requests anything else.

> **Exercise**
>
> Modify `handle_connection` such that only a request to "/" sends back `index.html`. All other requests should send back `404.html` instead.

Our code should now look like this:

```rust
// Filename: src/main.rs
// --snip--

fn handle_connection(mut stream: TcpStream) {
    let buf_reader = BufReader::new(&mut stream);
    let request_line = buf_reader.lines().next().unwrap().unwrap();

    if request_line == "GET / HTTP/1.1" {
        let status_line = "HTTP/1.1 200 OK";
        let contents = fs::read_to_string("hello.html").unwrap();
        let length = contents.len();

        let response = format!(
            "{status_line}\r\nContent-Length: {length}\r\n\r\n{contents}"
        );

        stream.write_all(response.as_bytes()).unwrap();
    } else {
        let status_line = "HTTP/1.1 404 NOT FOUND";
        let contents = fs::read_to_string("404.html").unwrap();
        let length = contents.len();

        let response = format!(
            "{status_line}\r\nContent-Length: {length}\r\n\r\n{contents}"
        );

        stream.write_all(response.as_bytes()).unwrap();
    }
}
```

With these changes, run your server again. Requesting _127.0.0.1:7878_ should return the contents of _hello.html_, and any other request, like _127.0.0.1:7878/foo_, should return the error HTML from _404.html_.

### A Touch of Refactoring

Let's refactor our code to remove repetition.

```rust
// --snip--

fn handle_connection(mut stream: TcpStream) {
    // --snip--

    let (status_line, filename) = if request_line == "GET / HTTP/1.1" {
        ("HTTP/1.1 200 OK", "hello.html")
    } else {
        ("HTTP/1.1 404 NOT FOUND", "404.html")
    };

    let contents = fs::read_to_string(filename).unwrap();
    let length = contents.len();

    let response =
        format!("{status_line}\r\nContent-Length: {length}\r\n\r\n{contents}");

    stream.write_all(response.as_bytes()).unwrap();
}
```

## Part 2: From Single-Threaded to Multithreaded

Right now, the server will process each request in turn, meaning it won’t process a second connection until the first is finished processing. If the server received more and more requests, this serial execution would be less and less optimal. If the server receives a request that takes a long time to process, subsequent requests will have to wait until the long request is finished, even if the new requests can be processed quickly.

### Simulating a Slow Request

Let's take a look how a slow request will affect other requests made to our current server implementation. A request sent to _/sleep_ will cause the server to sleep for 5 seconds before responding.

```rust
use std::{
    fs,
    io::{prelude::*, BufReader},
    net::{TcpListener, TcpStream},
    thread,
    time::Duration,
};
// --snip--

fn handle_connection(mut stream: TcpStream) {
    // --snip--

    let (status_line, filename) = match &request_line[..] {
        "GET / HTTP/1.1" => ("HTTP/1.1 200 OK", "index.html"),
        "GET /sleep HTTP/1.1" => {
            thread::sleep(Duration::from_secs(5));
            ("HTTP/1.1 200 OK", "index.html")
        }
        _ => ("HTTP/1.1 404 NOT FOUND", "404.html"),
    };

    // --snip--
}
```

Start the server. Then open two browser windows: one for *http://127.0.0.1:7878/* and the other for *http://127.0.0.1:7878/slee*p. If you enter the _/_ URI a few times, as before, you’ll see it respond quickly. But if you enter _/sleep_ and then load _/_, you’ll see that _/_ waits until sleep has slept for its full 5 seconds before loading.

There are multiple techniques we could use to avoid requests backing up behind a slow request; the one we’ll implement is a [thread pool](https://en.wikipedia.org/wiki/Thread_pool).

### What is a Thread Pool?

A thread pool is a group of spawned threads that are waiting and ready to handle a task. When the program receives a new task, it assigns one of the threads in the pool to the task, and that thread will process the task. The remaining threads in the pool are available to handle any other tasks that come in while the first thread is processing. When the first thread is done processing its task, it’s returned to the pool of idle threads, ready to handle a new task. A thread pool allows you to process connections concurrently, increasing the throughput of your server.

We’ll limit the number of threads in the pool to a small number to protect us from Denial of Service (DoS) attacks; if we had our program create a new thread for each request as it came in, someone making 10 million requests to our server could create havoc by using up all our server’s resources and grinding the processing of requests to a halt.

Rather than spawning unlimited threads, then, we’ll have a fixed number of threads waiting in the pool. Requests that come in are sent to the pool for processing. The pool will maintain a queue of incoming requests. Each of the threads in the pool will pop off a request from this queue, handle the request, and then ask the queue for another request. With this design, we can process up to `N` requests concurrently, where `N` is the number of threads. If each thread is responding to a long-running request, subsequent requests can still back up in the queue, but we’ve increased the number of long-running requests we can handle before reaching that point.

This technique is just one of many ways to improve the throughput of a web server. Other options you might explore are the [_fork/join model_](https://nus-cs2030s.github.io/2021-s2/37-forkjoin.html), the [_single-threaded async I/O model_](https://www.geeksforgeeks.org/how-the-single-threaded-non-blocking-io-model-works-in-nodejs/), or the _multi-threaded async I/O model_.

### Spawning a Thread for Each Request

First, let’s explore how our code might look if it did create a new thread for every connection. As mentioned earlier, this isn’t our final plan due to the problems with potentially spawning an unlimited number of threads, but it is a starting point to get a working multithreaded server first. Then we’ll add the thread pool as an improvement, and contrasting the two solutions will be easier. In the code below, we spawn a new thread to handle each stream within the `for` loop.

```rust
fn main() {
    let listener = TcpListener::bind("127.0.0.1:7878").unwrap();

    for stream in listener.incoming() {
        let stream = stream.unwrap();

        thread::spawn(|| {
            handle_connection(stream);
        });
    }
}
```

If you run this code and load _/sleep_ in your browser, then _/_ in two more browser tabs, you’ll indeed see that the requests to _/_ don’t have to wait for _/sleep_ to finish. However, as we mentioned, this will eventually overwhelm the system because you’d be making new threads without any limit.

### Creating a Finite Number of Threads with ThreadPool
