# Oki.py

Minimal, typed, functional and dynamic test library.

## Usage

```py
def main():
    suite = Suite()

    @suite.test()
    def adds_correctly(ctx):
        assert 2 + 2 == 4

    @suite.test()
    def adds_incorrectly(ctx):
        print("this must work")
        assert 2 + 2 == 5

    @suite.test()
    def it_doesnt_fail(ctx):
        print("hope this doesnt fail ...")
        print("oh, this will fail", file=sys.stderr)
        raise Exception("Expected failure.")

    @suite.test()
    def it_fails(ctx):
        with ctx.assert_raises():
            raise Exception("Expected failure.")

    suite.run()
```

Results in this output when run :

![test output screenshot](./assets/output.png)
