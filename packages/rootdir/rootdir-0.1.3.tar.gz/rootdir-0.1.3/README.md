## Find root directory simply

You can find the root directory intuitively, quickly and simply.

### Usage

1. Install by `pip install rootdir`
2. Add `__root__.py` to your root path.
3. `import rootdir`
4. use as `rootdit.root_dir(__file__)`

### example 1

If you need root directory, you could get it simply.

```python
import rootdir

if __name__ == "__main__":
    print(rootdir.root_dir(__file__))
```

### example 2

If you've found a directory for Python dependencies, you can solve it all at once with the following function.

```python
import rootdir
rootdir.root_dependency(__file__)
```

Now you can import Python dependencies from root directory. 

### sample

You can see the [sample code](https://github.com/meansoup/rootdir/tree/main/sample) implemented as shown below.

```
.
└── example/
├── a/
│   └── a_1.py
├── b/
│   ├── b_1/
│   │   ├── b_1_1/
│   │   │   └── b_1_1_1.py
│   │   └── b_1_2.py
│   └── b_2.py
├── main.py
└── __root__.py
```

```python
import rootdir
rootdir.root_dependency(__file__)

if __name__ == "__main__":
    print(rootdir.root_dir(__file__))
```

You can use upper code in any python file.
