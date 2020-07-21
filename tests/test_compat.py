import pytest

import click
from click._compat import should_strip_ansi
from click._compat import WIN
from click.shell_completion import bash_version_not_usable


@pytest.mark.skipif(
    bash_version_not_usable(), reason="Bash autocomplete not supported on bash < 4.4"
)
def test_bash_func_name():
    from click.shell_completion import get_completion_script

    @click.command()
    def foo_bar():
        pass

    script = get_completion_script(
        foo_bar, "foo-bar baz_blah", "_COMPLETE_VAR", "bash"
    ).strip()
    assert script.startswith("_foo_barbaz_blah_completion()")
    assert "_COMPLETE_VAR=complete $1" in script


def test_zsh_func_name():
    from click.shell_completion import get_completion_script

    @click.command()
    def foo_bar():
        pass

    script = get_completion_script(foo_bar, "foo-bar", "_COMPLETE_VAR", "zsh").strip()
    assert script.startswith("#compdef foo-bar")
    assert "compdef _foo_bar_completion foo-bar;" in script
    assert "(( ! $+commands[foo-bar] )) && return 1" in script


@pytest.mark.xfail(WIN, reason="Jupyter not tested/supported on Windows")
def test_is_jupyter_kernel_output():
    class JupyterKernelFakeStream:
        pass

    # implementation detail, aka cheapskate test
    JupyterKernelFakeStream.__module__ = "ipykernel.faked"
    assert not should_strip_ansi(stream=JupyterKernelFakeStream())
